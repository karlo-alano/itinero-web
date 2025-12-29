import os, requests, json, asyncio, random
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from pulp import *
from datetime import datetime, timedelta
import pytz

load_dotenv()
APIKEY = os.getenv('GOOGLE_API_KEY')

if not APIKEY:
    print("WARNING: GOOGLE_API_KEY environment variable not set!")
    print("Please set your Google API key in a .env file or environment variable")
    print("The application will not work without a valid Google API key")
search_url = "https://places.googleapis.com/v1/places:searchNearby"
routeMatrix_url = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
polyline_url = "https://routes.googleapis.com/directions/v2:computeRoutes"

app = Flask(__name__)

CORS(app, origins=[
    "https://itinero.site",
    "https://www.itinero.site",
    "https://api.itinero.site",
    "https://itinero-web.vercel.app" 
])

@app.route('/api', methods=['POST'])
def get_all_data():
    # Capture request timestamp
    request_time = datetime.now(pytz.utc)

    data = request.get_json()

    startingLocation = data['startingLocation']
    endingLocation = data['endingLocation']
    timeAllotted = data.get('timeAllotted')
    interestsArray = data.get('interests')
    rankingPreference = data.get('rankingPreference', 'distance')  # Default to distance if not provided

    # Calculate time frame in Philippine timezone
    time_frame = get_time_frame_and_timezone(request_time, timeAllotted)

    # Use cached hours search instead of live API
    results, other_results = search_with_cached_hours(
        interestsArray,
        startingLocation,
        endingLocation,
        rankingPreference,
        time_frame['start_time'],
        time_frame['end_time']
    )
    matrixData, distances, durations = trace_distance(results)
    path, total_distance, total_time, segment_distances, segment_durations = nearest_neighbor(distances, durations)
    total_travel_minutes = total_time / 60
    time_for_activities = timeAllotted - total_travel_minutes
    final_schedule = scheduling(path, results, time_for_activities, segment_durations)
    polylineString = polyline(final_schedule)
    
    print("OTHER RESULTS: ", other_results)
    return jsonify({
        "status": "success",
        "message": f"Successfully searched {len(interestsArray)} interests.",
        "request_time": request_time.isoformat(),
        "time_frame": {
            "start": time_frame['start_time'].isoformat(),
            "end": time_frame['end_time'].isoformat(),
            "timezone": "Asia/Manila"
        },
        "search_results": results,
        "other_results": other_results,
        "distance_matrix": matrixData,
        "distances": distances,
        "durations": durations,
        "path": path,
        "total_time": total_time,
        "total_distance": total_distance,
        "total_time_travel": total_time,
        "time_for_activities": time_for_activities,
        "final_schedule": final_schedule,
        "segments": {
            "durations": segment_durations,
            "distances": segment_distances
        },
        "polyline": polylineString
    }), 200

def get_time_frame_and_timezone(request_time, time_allotted):
    """Convert UTC request time to Philippine time and calculate time frame"""
    # Philippine Time is UTC+8
    PHILIPPINE_TIMEZONE = pytz.timezone('Asia/Manila')

    # Convert UTC to Philippine time
    local_start_time = request_time.astimezone(PHILIPPINE_TIMEZONE)

    # Calculate end time
    local_end_time = local_start_time + timedelta(hours=time_allotted)

    return {
        'start_time': local_start_time,
        'end_time': local_end_time,
        'timezone': PHILIPPINE_TIMEZONE
    }

def filter_establishments_by_preferences(interests_array, ranking_preference):
    """Load storeHours.json and filter by establishment types and ranking preference"""
    try:
        # Load cached establishment data
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cache_file_path = os.path.join(script_dir, "..", "database", "storeHours.json")

        with open(cache_file_path, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)

        filtered_establishments = {}

        # Filter by establishment types (interests) and ranking preference
        for establishment_type in interests_array:
            if establishment_type in cache_data['establishments']:
                # Get the ranking type (distance or popularity)
                ranking_key = ranking_preference.lower()  # 'distance' or 'popularity'

                if ranking_key in cache_data['establishments'][establishment_type]:
                    establishments = cache_data['establishments'][establishment_type][ranking_key]
                    filtered_establishments[establishment_type] = establishments

        return filtered_establishments

    except Exception as e:
        print(f"Error loading storeHours.json: {e}")
        return {}

def categorize_by_availability(establishments, start_time, end_time):
    """Categorize establishments by their availability during the time frame"""
    categorized = {
        'full': {},
        'partial': {},
        'unknown': {},
        'unavailable': {}
    }

    def is_establishment_available(opening_hours, check_start, check_end):
        """Check if establishment is available during the specified time"""
        if not opening_hours or 'periods' not in opening_hours:
            return 'unknown'

        # Convert times to minutes since midnight for easier comparison
        start_minutes = check_start.hour * 60 + check_start.minute
        end_minutes = check_end.hour * 60 + check_end.minute
        start_day = check_start.weekday()  # 0=Monday, 1=Tuesday, ..., 6=Sunday
        end_day = check_end.weekday()

        # Convert to Google format (0=Sunday, 1=Monday, ..., 6=Saturday)
        google_start_day = (start_day + 1) % 7
        google_end_day = (end_day + 1) % 7

        # Check if time frame spans multiple days
        if google_start_day != google_end_day:
            # Multi-day time frame - need to check each day
            return check_multi_day_availability(opening_hours, google_start_day, google_end_day, start_minutes, end_minutes)

        # Single day time frame
        day_periods = [p for p in opening_hours['periods'] if p['open']['day'] == google_start_day]

        if not day_periods:
            return 'unavailable'

        # Check if any period covers the entire time frame
        fully_covered = False
        partially_covered = False

        for period in day_periods:
            open_minutes = period['open']['hour'] * 60 + period['open']['minute']
            close_minutes = period['close']['hour'] * 60 + period['close']['minute']

            # Handle cases where closing time is next day (close_minutes < open_minutes)
            if close_minutes < open_minutes:
                close_minutes += 24 * 60  # Add 24 hours

            # Check full coverage
            if open_minutes <= start_minutes and close_minutes >= end_minutes:
                fully_covered = True
                break

            # Check partial coverage
            if (open_minutes < end_minutes and close_minutes > start_minutes):
                partially_covered = True

        if fully_covered:
            return 'full'
        elif partially_covered:
            return 'partial'
        else:
            return 'unavailable'

    def check_multi_day_availability(opening_hours, start_day, end_day, start_minutes, end_minutes):
        """Check availability across multiple days"""
        # For simplicity, check if establishment is open during both start and end times
        # This is a basic implementation - could be enhanced for more complex logic

        start_day_periods = [p for p in opening_hours['periods'] if p['open']['day'] == start_day]
        end_day_periods = [p for p in opening_hours['periods'] if p['open']['day'] == end_day]

        start_available = False
        end_available = False

        # Check start day availability (from start time to end of day)
        for period in start_day_periods:
            open_minutes = period['open']['hour'] * 60 + period['open']['minute']
            close_minutes = period['close']['hour'] * 60 + period['close']['minute']
            if close_minutes < open_minutes:
                close_minutes += 24 * 60
            if open_minutes <= start_minutes and close_minutes >= start_minutes:
                start_available = True
                break

        # Check end day availability (from start of day to end time)
        for period in end_day_periods:
            open_minutes = period['open']['hour'] * 60 + period['open']['minute']
            close_minutes = period['close']['hour'] * 60 + period['close']['minute']
            if close_minutes < open_minutes:
                close_minutes += 24 * 60
            if open_minutes <= end_minutes and close_minutes >= end_minutes:
                end_available = True
                break

        if start_available and end_available:
            return 'full'  # Available throughout the multi-day period
        elif start_available or end_available:
            return 'partial'  # Available on at least one day
        else:
            return 'unavailable'

    # Categorize all establishments
    for establishment_type, establishment_list in establishments.items():
        for establishment in establishment_list:
            availability = is_establishment_available(
                establishment.get('regularOpeningHours'),
                start_time,
                end_time
            )

            if availability not in categorized:
                categorized[availability][establishment_type] = []
            elif establishment_type not in categorized[availability]:
                categorized[availability][establishment_type] = []

            categorized[availability][establishment_type].append(establishment)

    return categorized

def select_itinerary_establishments(categorized_results):
    """Select main establishments randomly from available options"""
    main_results = []
    other_results = []
    warnings = []

    # Process each establishment type
    all_categories = set()
    for availability_type in categorized_results.values():
        all_categories.update(availability_type.keys())

    for category in all_categories:
        selected = None
        availability_status = None

        # 1. Try 'full' availability first
        # We use random.choice to pick ANY available option for maximum variety
        if category in categorized_results['full'] and categorized_results['full'][category]:
            candidates = categorized_results['full'][category]
            selected = random.choice(candidates).copy()
            availability_status = 'full'

        # 2. No full availability - Try partial
        elif category in categorized_results['partial'] and categorized_results['partial'][category]:
            warnings.append(f"No fully available places for {category}, using partial availability.")
            candidates = categorized_results['partial'][category]
            selected = random.choice(candidates).copy()
            availability_status = 'partial'

        # 3. Last resort - Try unknown
        elif category in categorized_results['unknown'] and categorized_results['unknown'][category]:
            warnings.append(f"No available places for {category}, using unknown availability.")
            candidates = categorized_results['unknown'][category]
            selected = random.choice(candidates).copy()
            availability_status = 'unknown'

        # If we found a selection, add it to main_results
        if selected:
            selected['availability_status'] = availability_status
            main_results.append({
                'interestType': category,
                'places': selected
            })
        else:
             warnings.append(f"No establishments found for {category} in any availability category")

    # --- Build other_results ---
    # We populate this with ALL other options that weren't picked as the main one
    
    # Helper to handle 'id' vs 'place_id' consistency
    def get_place_id(place_obj):
        return place_obj.get('id', place_obj.get('place_id'))

    for category in all_categories:
        category_other_results = []

        # Helper to check if a place is the one we just selected as the 'Main' result
        def is_selected_main(est):
            est_id = get_place_id(est)
            for main in main_results:
                if main['interestType'] == category and get_place_id(main['places']) == est_id:
                    return True
            return False

        # Add remaining 'Full' options to other_results (since we picked one randomly, the rest go here)
        if category in categorized_results['full']:
            for establishment in categorized_results['full'][category]:
                if not is_selected_main(establishment):
                    category_other_results.append(establishment)

        # Add remaining 'Partial' options
        if category in categorized_results['partial']:
            for establishment in categorized_results['partial'][category]:
                if not is_selected_main(establishment):
                    category_other_results.append(establishment)

        # Add remaining 'Unknown' options
        if category in categorized_results['unknown']:
            for establishment in categorized_results['unknown'][category]:
                if not is_selected_main(establishment):
                    category_other_results.append(establishment)

        if category_other_results:
            other_results.append({
                'interestType': category,
                'places': category_other_results
            })

    return {
        'main_results': main_results,
        'other_results': other_results,
        'warnings': warnings
    }

def search_with_cached_hours(interests_array, starting_location, ending_location, ranking_preference, start_time, end_time):
    """Main search function using cached establishment data with opening hours"""
    results_array = []
    filtered_place_array = []
    other_places_array = []

    # Add start location
    results_array.append({
        "interestType": "Start",
        "places": {
            "displayName": { "text": starting_location['name']},
            "formattedAddress": starting_location['address'],
            "id": starting_location.get('place_id', starting_location.get('id')), # Safety check
            "location": {
                "latitude": starting_location['lat'],
                "longitude": starting_location['lng']
            }
        }
    })

    # Filter establishments by preferences
    filtered_establishments = filter_establishments_by_preferences(interests_array, ranking_preference)

    # Categorize by availability
    categorized_results = categorize_by_availability(filtered_establishments, start_time, end_time)

    # Select establishments for itinerary
    selection_results = select_itinerary_establishments(categorized_results)

    # Add selected establishments to results array
    for result in selection_results['main_results']:
        # --- FIX: Don't crash if 'place_id' is missing ---
        # Your JSON already has 'id', so we only rename if 'place_id' exists
        if 'place_id' in result['places']:
            result['places']['id'] = result['places'].pop('place_id')
        
        results_array.append(result)

        # Add to filtered_place_array for compatibility
        filtered_place_array.append(result['places'])

    # Build other_places_array from other_results
    for other_result in selection_results['other_results']:
        for place in other_result['places']:
            # --- FIX: Don't crash if 'place_id' is missing ---
            if 'place_id' in place:
                place['id'] = place.pop('place_id')

        other_places_array.append(other_result)

    # Add end location
    results_array.append({
        "interestType": "End",
        "places": {
            "displayName": { "text": ending_location['name']},
            "formattedAddress": ending_location['address'],
            "id": ending_location.get('place_id', ending_location.get('id')), # Safety check
            "location": {
                "latitude": ending_location['lat'],
                "longitude": ending_location['lng']
            }
        }
    })

    return results_array, other_places_array

def search(interestsArray, startingLocation, endingLocation):
    center = {"lat": 14.59130,"lng": 120.97505 };
    resultsArray = []
    filtered_place_array = []
    otherPlacesArray = []
    
    if not request.is_json:
        return jsonify({"error": "Unsupported Media Type: Request must be JSON."}), 415
    
    resultsArray.append({
        "interestType": "Start",
        "places": {
            "displayName": { "text": startingLocation['name']},
            "formattedAddress": startingLocation['address'],
            "id": startingLocation['place_id'],
            "location": {
                "latitude": startingLocation['lat'],
                "longitude": startingLocation['lng']
            }
        }
    })
    
    for interest in interestsArray:
        params = {
            "includedTypes": interest,
            "maxResultCount": 10,
            "rankPreference": "DISTANCE",
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": center['lat'],
                        "longitude": center['lng']    
                    },
                    "radius": 700.0
                    
                }
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": APIKEY,
             "X-Goog-FieldMask": "places.displayName,places.location,places.formattedAddress,places.id"
        }
        
        try :
            api_response = requests.post(search_url, headers=headers, json=params)
            api_response.raise_for_status()
            responseData = api_response.json()
            api_place_data = responseData.get('places', [])
            
            filtered_place_array = [
                place for place in api_place_data
                if place.get('id') not in [startingLocation['place_id'], endingLocation['place_id']]
            ]
            
            randomizer = random.randint(0, len(filtered_place_array) - 1)
            final_place = filtered_place_array[randomizer]
            
            resultsArray.append({
                "interestType": interest,
                "places": final_place
            })
            
            otherPlacesArray.append({
                "interestType": interest,
                "places": filtered_place_array
            })
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {interest}: {e}")
            resultsArray.append({
                "interestType": interest,
                "places": [],
                "error": str(e)
            })
    resultsArray.append({
        "interestType": "End",
        "places": {
            "displayName": { "text": endingLocation['name']},
            "formattedAddress": endingLocation['address'],
            "id": endingLocation['place_id'],
            "location": {
                "latitude": endingLocation['lat'],
                "longitude": endingLocation['lng']
            }
        }
    }) 
    
    return resultsArray, otherPlacesArray    
            
def trace_distance(results):
    all_locations = [{"waypoint": {"placeId": result['places']['id']}} for result in results]
    destinationsArray = []
    for eachResult in results:
        destinationsArray.append(eachResult['places'])
           
    payload = {
    "origins": all_locations,
    "destinations": all_locations,
    "travelMode": "WALK"
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": APIKEY,
        "X-Goog-FieldMask": "originIndex,destinationIndex,duration,distanceMeters,status"
    }
    
    try:
        response = requests.post(routeMatrix_url, headers=headers, json=payload)
        response.raise_for_status()
        distanceMatrix = response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"External API request failed: {e}")
        return (
        {"error": "External API request failed", "details": str(e)},
        [[float('inf')]], 
        [[float('inf')]]
    )
    
    matrixResultsArray = []
    N = len(all_locations)
    distances = [[0] * N for _ in range(N)]
    durations = [[0] * N for _ in range(N)]
    
    for place in distanceMatrix: 
        o = place["originIndex"]
        d = place["destinationIndex"]
        if place.get('originIndex') is not None:
            distance_value = place.get("distanceMeters", 0)
            duration_value = place.get("duration", 0)
        else:
            distance_value = float('inf')
            duration_value = float('inf')

        distances[o][d] = distance_value
        durations[o][d] = int(duration_value.rstrip('s'))
        
        destination_index = place.get('destinationIndex')
        place_info = destinationsArray[destination_index]
        
        matrixResultsArray.append({
            "origin_index": place.get('originIndex'),
            "destination_index": destination_index,
            "place_name": place_info['displayName']['text'],    
            "destination_id": place_info.get('id'),
            "distance_meters": distance_value,
            "duration_seconds": duration_value,
            "status": place.get('status')
        })    
    return matrixResultsArray, distances, durations
             
def nearest_neighbor(distanceMatrix,durationsMatrix):
    n = len(durationsMatrix)
    start_node = 0
    end_node = n - 1
    
    path = [start_node]
    
    segment_durations = []
    segment_distances = []
    
    segment_distances.append(0)
    segment_durations.append(0)
    unvisited = set(range(1, n-1))
    
    current_node = start_node 
    
    while unvisited:
        min_duration = float('inf')
        nearest_neighbor = None
        
        for neighbor in unvisited:
            duration = durationsMatrix[current_node][neighbor]
            
            if duration < min_duration:
                min_duration = duration
                nearest_neighbor = neighbor
            
        if nearest_neighbor is not None:
            segment_durations.append(min_duration)
            segment_distances.append(distanceMatrix[current_node][nearest_neighbor])
            
            
            path.append(nearest_neighbor)
            unvisited.remove(nearest_neighbor)
            current_node = nearest_neighbor
        else:
            break
    if current_node != end_node:
        final_duration = durationsMatrix[current_node][end_node]
        final_distance = distanceMatrix[current_node][end_node]
        
        segment_durations.append(final_duration)
        segment_distances.append(final_distance)    
        
    path.append(end_node)
    
    total_distance = sum(distanceMatrix[path[i]][path[i + 1]]
                            for i in range(len(path) - 1))
    
    total_duration = sum(durationsMatrix[path[i]][path[i + 1]]
                            for i in range(len(path) - 1))
    
    return path, total_distance, total_duration, segment_distances, segment_durations    


TYPE_PARAMETERS = {
    "restaurant":  {"multiplier": 1.5, "min_duration": 45},  
    "cafe":        {"multiplier": 1.2, "min_duration": 30}, 
    "museum":      {"multiplier": 0.8, "min_duration": 60},  
    "park":        {"multiplier": 1.0, "min_duration": 20},  
    "church":       {"multiplier": 1.1, "min_duration": 30},
    "tourist_attraction": {"multiplier": 1.0, "min_duration": 30},
    "Start": {"multiplier": 1.0, "min_duration": 0},
    "End":   {"multiplier": 1.0, "min_duration": 0}
}
                
def scheduling(path, results, time_for_activities, segment_durations):
    MANILA_TZ = pytz.timezone('Asia/Manila')

    timeNow = datetime.now(MANILA_TZ)

    timeHour = timeNow.hour
    timeMinutes = timeNow.minute
    
    T_target = time_for_activities 
    
    scheduled_stops = [results[i] for i in path]
    schedulable_periods = [
        item for item in scheduled_stops 
        if item['interestType'] not in ['Start', 'End']
    ]
    N = len(schedulable_periods)

    if N == 0 or T_target <= 0:
        final_schedule = []
        current_time = timeNow
        for i, item in enumerate(scheduled_stops):
            item['scheduled_activity_minutes'] = 0
            item['travel_time_seconds'] = segment_durations[i] if i < len(segment_durations) else 0
            item['arrival_time'] = current_time.strftime("%I:%M %p")
            item['leave_time'] = current_time.strftime("%I:%M %p")
            final_schedule.append(item)
        return final_schedule


    initial_equal_duration = T_target / N 
    period_data = {}
    for period_info in schedulable_periods:
        p_id = period_info['places']['id']
        p_type = period_info['interestType']
        params = TYPE_PARAMETERS.get(p_type, {"multiplier": 1.0, "min_duration": 10})
        period_data[p_id] = {
            "orig_duration": initial_equal_duration, "multiplier": params["multiplier"],
            "min_duration": params["min_duration"], "type": p_type
        }
    lp_period_ids = list(period_data.keys())

    # LINEAR PROGRAMMING MODEL
    prob = LpProblem("Scheduling_Resizing_Optimization", LpMinimize)
    x = LpVariable.dict("FinalDuration", lp_period_ids, lowBound=0) 
    d_inc = LpVariable.dict("IncreaseDeviation", lp_period_ids, lowBound=0)
    d_dec = LpVariable.dict("DecreaseDeviation", lp_period_ids, lowBound=0)
    
    objective = lpSum([ (d_inc[p_id] + d_dec[p_id]) / period_data[p_id]["multiplier"] for p_id in lp_period_ids ])
    prob += objective, "Minimize_Weighted_Resizing_Deviation"
    prob += lpSum([x[p_id] for p_id in lp_period_ids]) == T_target, "Total_Schedule_Time"
    for p_id in lp_period_ids:
        min_dur = period_data[p_id]["min_duration"]
        orig_dur = period_data[p_id]["orig_duration"]
        prob += x[p_id] >= min_dur, f"MinDuration_Constraint_{p_id}"
        prob += x[p_id] - orig_dur == d_inc[p_id] - d_dec[p_id], f"Deviation_Linkage_{p_id}"

    # SOLVE AND MAP
    prob.solve()
    final_schedule_map = {}
    if LpStatus[prob.status] == "Optimal":
        for p_id in lp_period_ids:
            final_schedule_map[p_id] = value(x[p_id])
    else:
        for p_id in lp_period_ids:
             final_schedule_map[p_id] = period_data[p_id]["min_duration"]
    
    final_schedule = []
    
    current_arrival_time = timeNow 
    
    for i, item in enumerate(scheduled_stops):
        p_id = item['places']['id']
        p_type = item['interestType']
        
        # Determine Activity Time
        activity_minutes = 0
        if p_type not in ['Start', 'End']:
            activity_minutes = final_schedule_map.get(p_id, 0)
        
        # Calculate Absolute Times
        
        # The arrival time at THIS location
        item['arrival_time'] = current_arrival_time.strftime("%I:%M %p")
        
        # The time spent at this stop
        activity_duration_delta = timedelta(minutes=activity_minutes)
        
        # The leave time is Arrival Time + Activity Duration
        leave_time = current_arrival_time + activity_duration_delta
        item['leave_time'] = leave_time.strftime("%I:%M %p")
        
        # Travel time FROM this stop TO the next one
        travel_out_seconds = segment_durations[i+1] if i + 1 < len(segment_durations) else 0
        travel_duration_delta = timedelta(seconds=travel_out_seconds)
        
        current_arrival_time = leave_time + travel_duration_delta 
        
        # Final Output Formatting
        item['scheduled_activity_minutes'] = activity_minutes
        
        # Travel time is the time spent traveling *to the next stop*
        item['travel_time_to_next_stop_seconds'] = travel_out_seconds
        
            
        final_schedule.append(item)
    
    return final_schedule

def polyline(route):
    lastIndex = len(route) - 1
    
    origin = {
        "location": {
            "latLng": {
                "latitude": route[0]['places']['location']['latitude'],
                "longitude": route[0]['places']['location']['longitude']
            }
        }
    }
    destination = {
        "location": {
            "latLng": {
                "latitude": route[lastIndex]['places']['location']['latitude'],
                "longitude": route[lastIndex]['places']['location']['longitude']
            }
        }
    }
    intermediates = [
        {
            "location": {
                "latLng": {
                    "latitude": item['places']['location']['latitude'],
                    "longitude": item['places']['location']['longitude']
                }
            } 
        }
        for i, item in enumerate(route)
        if i not in (0, lastIndex)
    ]
    payload = {
        "origin": origin,
        "destination": destination,
        "intermediates": intermediates,
        "travelMode": "WALK",
    }
    
    headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": APIKEY,
            "X-Goog-FieldMask": "routes.polyline.encodedPolyline"
    }
    
    try:
        response = requests.post(polyline_url, headers=headers, json=payload)
        response.raise_for_status()
        polyline = response.json()

        encoded_polyline = polyline['routes'][0]['polyline']['encodedPolyline']

        if not encoded_polyline:
            print("No polyline found in response.")
            return None

        return encoded_polyline

        
    except requests.exceptions.RequestException as e:
        print(f"External API request failed: {e}")
     
@app.route('/api/recalculate', methods=['POST'])
def recalculate_itinerary():
    try:
        print("Recalculate endpoint called")
        data = request.get_json()
        print(f"Received data keys: {list(data.keys()) if data else 'No data'}")

        if not data or 'ordered_stops' not in data:
            raise ValueError("Missing 'ordered_stops' in request data")

        ordered_stops = data['ordered_stops']
        time_allotted = data.get('timeAllotted')

        if not ordered_stops:
            raise ValueError("ordered_stops is empty")

        if time_allotted is None:
            raise ValueError("timeAllotted is missing")

        if not APIKEY:
            print("WARNING: Google API key not configured, using mock data for testing")
            # Return mock data for testing when API key is missing
            mock_final_schedule = []
            for i, stop in enumerate(ordered_stops):
                mock_stop = stop.copy()
                mock_stop['scheduled_activity_minutes'] = 30 if stop['interestType'] not in ['Start', 'End'] else 0
                mock_stop['travel_time_to_next_stop_seconds'] = 300  # 5 minutes
                mock_stop['arrival_time'] = f"{9 + i}:00 AM"
                mock_stop['leave_time'] = f"{9 + i}:30 AM" if stop['interestType'] not in ['Start', 'End'] else f"{9 + i}:00 AM"
                mock_final_schedule.append(mock_stop)

            return jsonify({
                "status": "success",
                "message": f"Successfully recalculated itinerary with {len(ordered_stops)} stops (MOCK DATA - API key missing).",
                "search_results": ordered_stops,
                "distance_matrix": [],
                "distances": [],
                "durations": [],
                "path": list(range(len(ordered_stops))),
                "total_time": len(ordered_stops) * 300,
                "total_distance": len(ordered_stops) * 500,
                "total_time_travel": len(ordered_stops) * 300,
                "time_for_activities": time_allotted - (len(ordered_stops) * 300 / 60),
                "final_schedule": mock_final_schedule,
                "segments": {
                    "durations": [300] * (len(ordered_stops) - 1) + [0],
                    "distances": [500] * (len(ordered_stops) - 1) + [0]
                },
                "polyline": "mock_polyline_data"
            }), 200

        print(f"Recalculating itinerary with {len(ordered_stops)} stops")
        print(f"Time allotted: {time_allotted}")
        print(f"Sample stop: {ordered_stops[0] if ordered_stops else 'No stops'}")
        print(f"Full request data: {data}")

        # Use the provided ordered stops directly (no search needed)
        # Calculate distances and durations for the ordered stops
        print(f"Calling trace_distance with ordered_stops")
        matrix_data, distances, durations = trace_distance(ordered_stops)
        print(f"trace_distance completed successfully")

        # Since stops are already in the desired order, path is sequential [0, 1, 2, ..., n-1]
        path = list(range(len(ordered_stops)))

        # Calculate path metrics
        total_distance = sum(distances[path[i]][path[i + 1]] for i in range(len(path) - 1))
        total_time = sum(durations[path[i]][path[i + 1]] for i in range(len(path) - 1))

        # Calculate segment distances and durations
        segment_distances = [distances[path[i]][path[i + 1]] for i in range(len(path) - 1)]
        segment_durations = [durations[path[i]][path[i + 1]] for i in range(len(path) - 1)]

        # Add dummy first elements for start (to match original format)
        segment_distances.insert(0, 0)
        segment_durations.insert(0, 0)

        # Recalculate scheduling with new distances
        total_travel_minutes = total_time / 60
        time_for_activities = time_allotted - total_travel_minutes

        final_schedule = scheduling(path, ordered_stops, time_for_activities, segment_durations)

        # Generate new polyline
        polyline_string = polyline(final_schedule)

        print(f"Recalculation complete - new total distance: {total_distance} meters")

        # Return JSON in the same format as the original /api endpoint
        return jsonify({
            "status": "success",
            "message": f"Successfully recalculated itinerary with {len(ordered_stops)} stops.",
            "search_results": ordered_stops,
            "distance_matrix": matrix_data,
            "distances": distances,
            "durations": durations,
            "path": path,
            "total_time": total_time,
            "total_distance": total_distance,
            "total_time_travel": total_time,
            "time_for_activities": time_for_activities,
            "final_schedule": final_schedule,
            "segments": {
                "durations": segment_durations,
                "distances": segment_distances
            },
            "polyline": polyline_string
        }), 200

    except Exception as e:
        print(f"Error in recalculate_itinerary: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}",
            "error_type": type(e).__name__
        }), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"Google API Key configured: {APIKEY is not None}")
    app.run(debug=True, host='0.0.0.0', port=5000)