import os, requests, json, asyncio, random
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from pulp import *
from datetime import datetime, timedelta
import pytz, time

load_dotenv()
APIKEY = os.getenv('GOOGLE_API_KEY')

if not APIKEY:
    print("WARNING: GOOGLE_API_KEY environment variable not set!")

search_url = "https://places.googleapis.com/v1/places:searchNearby"
routeMatrix_url = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
polyline_url = "https://routes.googleapis.com/directions/v2:computeRoutes"

app = Flask(__name__)

CORS(app, origins=[
    "https://itinero.site",
    "https://www.itinero.site",
    "https://api.itinero.site",
    "https://itinero-web.vercel.app",
    "http://localhost:5173"
])

# --- CONFIGURATION ---
TYPE_PARAMETERS = {
    "restaurant":  {"multiplier": 1.5, "min_duration": 60},  
    "cafe":        {"multiplier": 1.2, "min_duration": 45}, 
    "museum":      {"multiplier": 0.8, "min_duration": 90},  
    "park":        {"multiplier": 1.0, "min_duration": 45},  
    "church":      {"multiplier": 1.1, "min_duration": 30},
    "tourist_attraction": {"multiplier": 1.0, "min_duration": 60},
    "Start": {"multiplier": 1.0, "min_duration": 0},
    "End":   {"multiplier": 1.0, "min_duration": 0}
}

# --- HELPER: TIME FRAME ---
def get_time_frame_and_timezone(request_time, time_allotted):
    PHILIPPINE_TIMEZONE = pytz.timezone('Asia/Manila')
    local_start_time = request_time.astimezone(PHILIPPINE_TIMEZONE)
    local_end_time = local_start_time + timedelta(hours=time_allotted)

    return {
        'start_time': local_start_time,
        'end_time': local_end_time,
        'timezone': PHILIPPINE_TIMEZONE
    }

# --- HELPER: DATABASE LOADER ---
def get_store_hours_data():
    """Helper to load the JSON database reliably"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cache_file_path = os.path.join(script_dir, "database", "storeHours.json") 
        if not os.path.exists(cache_file_path):
             cache_file_path = os.path.join(script_dir, "..", "database", "storeHours.json")
        
        with open(cache_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading storeHours.json: {e}")
        return None

# --- HELPER: FILTERING ---
def filter_establishments_by_preferences(interests_array, ranking_preference):
    cache_data = get_store_hours_data()
    if not cache_data: return {}

    filtered_establishments = {}
    for establishment_type in interests_array:
        if establishment_type in cache_data['establishments']:
            ranking_key = ranking_preference.lower()
            if ranking_key in cache_data['establishments'][establishment_type]:
                establishments = cache_data['establishments'][establishment_type][ranking_key]
                filtered_establishments[establishment_type] = establishments

    return filtered_establishments

# --- HELPER: AVAILABILITY (STRICTER) ---
def categorize_by_availability(establishments, start_time, end_time):
    """Categorize establishments by availability, checking previous day spillover"""
    categorized = {
        'full': {},
        'partial': {},
        'unknown': {},
        'unavailable': {}
    }

    def is_establishment_available(opening_hours, check_start, check_end):
        if not opening_hours or 'periods' not in opening_hours:
            return 'unknown'

        start_minutes = check_start.hour * 60 + check_start.minute
        end_minutes = check_end.hour * 60 + check_end.minute
        
        # Get the correct day - use the actual date, not just weekday
        check_date = check_start.date()
        start_day_py = check_start.weekday()
        google_current_day = (start_day_py + 1) % 7  # Monday=0 -> 1, etc.

        relevant_periods = []

        # Only get periods for the CURRENT day
        current_day_periods = [p for p in opening_hours['periods'] if p['open']['day'] == google_current_day]
        for period in current_day_periods:
            open_m = period['open']['hour'] * 60 + period['open']['minute']
            close_m = period['close']['hour'] * 60 + period['close']['minute']
            if close_m < open_m:  # Overnight - closes next day
                close_m += 1440
            relevant_periods.append((open_m, close_m))

        # Handle places that opened yesterday and close today (like 24-hour places or late-night spots)
        google_prev_day = (google_current_day - 1) % 7
        yesterday_periods = [p for p in opening_hours['periods'] if p['open']['day'] == google_prev_day]
        for period in yesterday_periods:
            open_m = period['open']['hour'] * 60 + period['open']['minute']
            close_m = period['close']['hour'] * 60 + period['close']['minute']
            if close_m < open_m:  # This period crosses midnight
                # Only include the portion that extends into today
                relevant_periods.append((0, close_m))

        if not relevant_periods:
            return 'unavailable'

        # Now check availability for the requested time window
        fully_covered = False
        partially_covered = False
        
        MIN_AVAILABLE_MINUTES = 45 

        for open_m, close_m in relevant_periods:
            # Full coverage: place is open throughout the entire requested window
            if open_m <= start_minutes and close_m >= end_minutes:
                fully_covered = True
                break
            
            # Partial coverage: place overlaps with requested window for at least MIN_AVAILABLE_MINUTES
            overlap_start = max(open_m, start_minutes)
            overlap_end = min(close_m, end_minutes)
            
            if overlap_end > overlap_start:
                duration_overlap = overlap_end - overlap_start
                if duration_overlap >= MIN_AVAILABLE_MINUTES:
                    partially_covered = True

        if fully_covered:
            return 'full'
        elif partially_covered:
            return 'partial'
        else:
            return 'unavailable'

    for establishment_type, establishment_list in establishments.items():
        for establishment in establishment_list:
            availability = is_establishment_available(
                establishment.get('regularOpeningHours'),
                start_time,
                end_time
            )

            if availability not in categorized: categorized[availability] = {}
            if establishment_type not in categorized[availability]: 
                categorized[availability][establishment_type] = []
            
            categorized[availability][establishment_type].append(establishment)

    return categorized

def select_itinerary_establishments(categorized_results, start_time):
    main_results = []
    other_results = []
    warnings = []
    
    current_hour = start_time.hour
    is_late_night = (current_hour >= 21 or current_hour < 5)

    all_categories = set()
    for availability_type in categorized_results.values():
        all_categories.update(availability_type.keys())

    for category in all_categories:
        selected = None
        availability_status = None

        if category in categorized_results['full'] and categorized_results['full'][category]:
            candidates = categorized_results['full'][category]
            selected = random.choice(candidates).copy()
            availability_status = 'full'
        elif category in categorized_results['partial'] and categorized_results['partial'][category]:
            warnings.append(f"No fully available places for {category}, using partial.")
            candidates = categorized_results['partial'][category]
            selected = random.choice(candidates).copy()
            availability_status = 'partial'
        elif category in categorized_results['unknown'] and categorized_results['unknown'][category]:
            if is_late_night:
                warnings.append(f"Late night: Skipping 'Unknown' places for {category}.")
            else:
                warnings.append(f"No available places for {category}, using unknown.")
                candidates = categorized_results['unknown'][category]
                selected = random.choice(candidates).copy()
                availability_status = 'unknown'

        if selected:
            selected['availability_status'] = availability_status
            main_results.append({
                'interestType': category,
                'places': selected
            })
        else:
             warnings.append(f"No establishments found for {category}")

    def get_place_id(place_obj):
        return place_obj.get('id', place_obj.get('place_id'))

    for category in all_categories:
        category_other_results = []
        def is_selected_main(est):
            est_id = get_place_id(est)
            for main in main_results:
                if main['interestType'] == category and get_place_id(main['places']) == est_id:
                    return True
            return False

        for status in ['full', 'partial', 'unknown']:
            if category in categorized_results[status]:
                for establishment in categorized_results[status][category]:
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
    results_array = []
    filtered_place_array = []
    other_places_array = []

    # Start
    results_array.append({
        "interestType": "Start",
        "places": {
            "displayName": { "text": starting_location['name']},
            "formattedAddress": starting_location['address'],
            "id": starting_location.get('place_id', starting_location.get('id')), 
            "location": {
                "latitude": starting_location['lat'],
                "longitude": starting_location['lng']
            }
        }
    })

    filtered_establishments = filter_establishments_by_preferences(interests_array, ranking_preference)
    categorized_results = categorize_by_availability(filtered_establishments, start_time, end_time)
    
    selection_results = select_itinerary_establishments(categorized_results, start_time)

    for result in selection_results['main_results']:
        if 'place_id' in result['places']:
            result['places']['id'] = result['places'].pop('place_id')
        results_array.append(result)
        filtered_place_array.append(result['places'])

    for other_result in selection_results['other_results']:
        for place in other_result['places']:
            if 'place_id' in place:
                place['id'] = place.pop('place_id')
        other_places_array.append(other_result)

    # End
    results_array.append({
        "interestType": "End",
        "places": {
            "displayName": { "text": ending_location['name']},
            "formattedAddress": ending_location['address'],
            "id": ending_location.get('place_id', ending_location.get('id')),
            "location": {
                "latitude": ending_location['lat'],
                "longitude": ending_location['lng']
            }
        }
    })

    return results_array, other_places_array

# --- HELPER: ROUTING ---
def trace_distance(results):
    all_locations = [{"waypoint": {"placeId": result['places']['id']}} for result in results]
    destinationsArray = [result['places'] for result in results]
            
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
        return ({"error": str(e)}, [[float('inf')]], [[float('inf')]])
    
    matrixResultsArray = []
    N = len(all_locations)
    distances = [[0] * N for _ in range(N)]
    durations = [[0] * N for _ in range(N)]
    
    for place in distanceMatrix: 
        o = place.get("originIndex")
        d = place.get("destinationIndex")
        if o is not None and d is not None:
            distance_value = place.get("distanceMeters", 0)
            duration_value = place.get("duration", "0s")
            
            distances[o][d] = distance_value
            durations[o][d] = int(duration_value.rstrip('s'))
            
            place_info = destinationsArray[d]
            matrixResultsArray.append({
                "origin_index": o,
                "destination_index": d,
                "place_name": place_info['displayName']['text'],    
                "destination_id": place_info.get('id'),
                "distance_meters": distance_value,
                "duration_seconds": duration_value,
                "status": place.get('status')
            })    
            
    return matrixResultsArray, distances, durations
             
def nearest_neighbor(distanceMatrix, durationsMatrix):
    n = len(durationsMatrix)
    start_node = 0
    end_node = n - 1
    
    path = [start_node]
    segment_durations = [0]
    segment_distances = [0]
    
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
    
    total_distance = sum(distanceMatrix[path[i]][path[i + 1]] for i in range(len(path) - 1))
    total_duration = sum(durationsMatrix[path[i]][path[i + 1]] for i in range(len(path) - 1))
    
    return path, total_distance, total_duration, segment_distances, segment_durations    

def scheduling(path, results, time_for_activities, segment_durations):
    MANILA_TZ = pytz.timezone('Asia/Manila')
    timeNow = datetime.now(MANILA_TZ)
    
    scheduled_stops = [results[i] for i in path]
    schedulable_periods = [
        item for item in scheduled_stops 
        if item['interestType'] not in ['Start', 'End']
    ]
    
    has_manual_durations = len(schedulable_periods) > 0 and 'duration' in schedulable_periods[0]
    final_schedule_map = {}

    if has_manual_durations:
        print("Manual durations detected.")
        for item in schedulable_periods:
            p_id = item['places']['id']
            duration_seconds = item.get('duration', 0)
            final_schedule_map[p_id] = duration_seconds / 60
    else:
        T_target = time_for_activities 
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
                "orig_duration": initial_equal_duration, 
                "multiplier": params["multiplier"],
                "min_duration": params["min_duration"], 
                "type": p_type
            }
        
        lp_period_ids = list(period_data.keys())

        # Compression
        total_min_needed = sum(d["min_duration"] for d in period_data.values())
        if total_min_needed > T_target:
            compression_factor = (T_target / total_min_needed) * 0.99
            for p_id in lp_period_ids:
                period_data[p_id]["min_duration"] *= compression_factor
                period_data[p_id]["orig_duration"] *= compression_factor
        
        # LP SOLVER
        prob = LpProblem("Scheduling", LpMinimize)
        x = LpVariable.dict("FinalDuration", lp_period_ids, lowBound=0) 
        d_inc = LpVariable.dict("Increase", lp_period_ids, lowBound=0)
        d_dec = LpVariable.dict("Decrease", lp_period_ids, lowBound=0)
        
        prob += lpSum([ (d_inc[p_id] + d_dec[p_id]) / period_data[p_id]["multiplier"] for p_id in lp_period_ids ])
        prob += lpSum([x[p_id] for p_id in lp_period_ids]) == T_target
        
        for p_id in lp_period_ids:
            prob += x[p_id] >= period_data[p_id]["min_duration"]
            prob += x[p_id] - period_data[p_id]["orig_duration"] == d_inc[p_id] - d_dec[p_id]

        prob.solve()
        
        if LpStatus[prob.status] == "Optimal":
            for p_id in lp_period_ids:
                final_schedule_map[p_id] = value(x[p_id])
        else:
            for p_id in lp_period_ids:
                final_schedule_map[p_id] = T_target / N

    # Timestamp Generation
    final_schedule = []
    current_arrival_time = timeNow 
    
    for i, item in enumerate(scheduled_stops):
        p_id = item['places']['id']
        p_type = item['interestType']
        
        activity_minutes = 0
        if p_type not in ['Start', 'End']:
            activity_minutes = final_schedule_map.get(p_id, 0)
        
        item['arrival_time'] = current_arrival_time.strftime("%I:%M %p")
        
        leave_time = current_arrival_time + timedelta(minutes=activity_minutes)
        item['leave_time'] = leave_time.strftime("%I:%M %p")
        
        travel_out_seconds = segment_durations[i+1] if i + 1 < len(segment_durations) else 0
        current_arrival_time = leave_time + timedelta(seconds=travel_out_seconds)
        
        item['scheduled_activity_minutes'] = activity_minutes
        
        if has_manual_durations and p_type not in ['Start', 'End']:
             item['duration'] = activity_minutes * 60
        
        item['travel_time_to_next_stop_seconds'] = travel_out_seconds
        final_schedule.append(item)
    
    return final_schedule

# --- FIX 3: POST-SCHEDULE VALIDATION ---
def validate_arrival_times(schedule, request_time):
    """
    Checks arrival times against store hours.
    Flags locations that will be closed by the time the user arrives.
    """
    cache_data = get_store_hours_data()
    if not cache_data: return schedule

    # Flatten cache for easy ID lookup
    hours_map = {}
    for cat, rankings in cache_data['establishments'].items():
        for r_key, places in rankings.items():
            for p in places:
                p_id = p.get('id', p.get('place_id'))
                hours_map[p_id] = p.get('regularOpeningHours')

    for stop in schedule:
        if stop['interestType'] in ['Start', 'End']: continue
        
        place_id = stop['places']['id']
        arrival_str = stop['arrival_time'] 
        
        try:
            arrival_dt = datetime.strptime(arrival_str, "%I:%M %p")
            # Combine with request_time date
            arrival_time = request_time.replace(
                hour=arrival_dt.hour, 
                minute=arrival_dt.minute, 
                second=0, 
                microsecond=0
            )
            # Handle day rollover
            if arrival_time < request_time and arrival_time.hour < 12:
                arrival_time += timedelta(days=1)
        except ValueError:
            continue

        opening_hours = hours_map.get(place_id)
        if not opening_hours: continue

        arrival_minutes = arrival_time.hour * 60 + arrival_time.minute
        google_day = (arrival_time.weekday() + 1) % 7
        
        is_open = False
        closing_time_str = "unknown"

        if 'periods' in opening_hours:
            for period in opening_hours['periods']:
                if period['open']['day'] == google_day:
                    open_m = period['open']['hour'] * 60 + period['open']['minute']
                    close_m = period['close']['hour'] * 60 + period['close']['minute']
                    
                    if close_m < open_m: close_m += 1440
                    
                    # Strict check: Open at arrival, and stays open for 30 mins
                    if open_m <= arrival_minutes < (close_m - 30):
                        is_open = True
                        break
                    else:
                        h = period['close']['hour']
                        m = period['close']['minute']
                        closing_time_str = f"{h:02d}:{m:02d}"

        if not is_open:
            stop['warning'] = f"Caution: This location may be closed (Closes around {closing_time_str})."
            stop['is_closed_on_arrival'] = True

    return schedule

def polyline(route):
    if len(route) < 2: return None
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
        polyline_res = response.json()
        return polyline_res.get('routes', [{}])[0].get('polyline', {}).get('encodedPolyline')
    except Exception as e:
        print(f"Polyline Error: {e}")
        return None

# --- MAIN ROUTES ---

@app.route('/api', methods=['POST'])
def get_all_data():
    random.seed(int(time.time() * 1000000) % 1000000)
    request_time = datetime.now(pytz.utc)
    data = request.get_json()

    startingLocation = data['startingLocation']
    endingLocation = data['endingLocation']
    timeAllotted = data.get('timeAllotted')
    interestsArray = data.get('interests')
    rankingPreference = data.get('rankingPreference', 'distance')

    # 1. Calculate time frame
    time_frame = get_time_frame_and_timezone(request_time, timeAllotted)

    # 2. Search & Filter
    results, other_results = search_with_cached_hours(
        interestsArray,
        startingLocation,
        endingLocation,
        rankingPreference,
        time_frame['start_time'],
        time_frame['end_time']
    )

    # --- FIX 1: BYPASS IF NO OPEN LOCATIONS ---
    # Check if we only have Start and End (Len <= 2)
    if len(results) <= 2:
        return jsonify({
            "status": "empty",
            "message": "It looks like most places are closed at this time.",
            "search_results": [],
            "final_schedule": [],
            "other_results": []
        }), 200

    # 3. Calculate Distances
    matrixData, distances, durations = trace_distance(results)

    # 4. Route Optimization (Nearest Neighbor)
    path, total_distance, total_time, segment_distances, segment_durations = nearest_neighbor(distances, durations)
    
    total_travel_minutes = total_time / 60
    time_for_activities = timeAllotted - total_travel_minutes

    # 5. Scheduling
    final_schedule = scheduling(path, results, time_for_activities, segment_durations)
    
    # --- FIX 3: VALIDATE ARRIVAL TIMES ---
    # Check if stops are actually open at the scheduled arrival time
    final_schedule = validate_arrival_times(final_schedule, request_time.astimezone(pytz.timezone('Asia/Manila')))

    # 6. Generate Polyline
    polylineString = polyline(final_schedule)
    
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

@app.route('/api/recalculate', methods=['POST'])
def recalculate_itinerary():
    try:
        data = request.get_json()
        ordered_stops = data['ordered_stops']
        time_allotted = data.get('timeAllotted')
        
        # Recalculate Logic
        matrix_data, distances, durations = trace_distance(ordered_stops)
        path = list(range(len(ordered_stops)))
        
        total_distance = sum(distances[path[i]][path[i + 1]] for i in range(len(path) - 1))
        total_time = sum(durations[path[i]][path[i + 1]] for i in range(len(path) - 1))
        
        # --- CALCULATE SEGMENTS ---
        segment_distances = [0] + [distances[path[i]][path[i + 1]] for i in range(len(path) - 1)]
        segment_durations = [0] + [durations[path[i]][path[i + 1]] for i in range(len(path) - 1)]

        total_travel_minutes = total_time / 60
        time_for_activities = time_allotted - total_travel_minutes

        final_schedule = scheduling(path, ordered_stops, time_for_activities, segment_durations)
        
        # Validate Arrival Times
        request_time = datetime.now(pytz.timezone('Asia/Manila'))
        final_schedule = validate_arrival_times(final_schedule, request_time)

        polyline_string = polyline(final_schedule)

        return jsonify({
            "status": "success",
            "message": "Recalculated",
            "search_results": ordered_stops,
            "distances": distances,
            "durations": durations,
            "total_time": total_time,
            "total_distance": total_distance,
            "final_schedule": final_schedule,
            # --- THE MISSING PIECE ---
            "segments": {
                "durations": segment_durations,
                "distances": segment_distances
            },
            # -------------------------
            "polyline": polyline_string
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)