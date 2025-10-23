import os, requests, json, asyncio, random
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from pulp import *
from datetime import datetime, timedelta

load_dotenv()
APIKEY = os.getenv('GOOGLE_API_KEY')
search_url = "https://places.googleapis.com/v1/places:searchNearby"
routeMatrix_url = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
polyline_url = "https://routes.googleapis.com/directions/v2:computeRoutes"

app = Flask(__name__)



@app.route('/api', methods=['POST'])
def get_all_data():
    data = request.get_json()
    
    startingLocation = data['startingLocation']
    endingLocation = data['endingLocation']
    timeAllotted = data.get('timeAllotted')
    interestsArray = data.get('interests')
    

    
    results, other_results = search(interestsArray, startingLocation, endingLocation)
    matrixData, distances, durations = trace_distance(results)
    path, total_distance, total_time, segment_distances, segment_durations = nearest_neighbor(distances, durations)
    total_travel_minutes = total_time / 60
    time_for_activities = timeAllotted - total_travel_minutes
    final_schedule = scheduling(path, results, time_for_activities, segment_durations)
    polylineString = polyline(final_schedule)
    
    return jsonify({
        "status": "success",
        "message": f"Successfully searched {len(interestsArray)} interests.",
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
        [[float('inf')]],  # placeholder 2D list
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
    "restaurant":  {"multiplier": 1.5, "min_duration": 45},  # Highly flexible, needs min 45 min
    "cafe":        {"multiplier": 1.2, "min_duration": 30},  # Flexible, min 30 min
    "museum":      {"multiplier": 0.8, "min_duration": 60},  # Less flexible, high min 1 hour
    "park":        {"multiplier": 1.0, "min_duration": 20},  # Standard
    "church":       {"multiplier": 1.1, "min_duration": 30},
    "tourist_attraction": {"multiplier": 1.0, "min_duration": 30},
    "Start": {"multiplier": 1.0, "min_duration": 0},
    "End":   {"multiplier": 1.0, "min_duration": 0}
}
                
def scheduling(path, results, time_for_activities, segment_durations):
    
    # --- Time Setup (RETAINING USER'S REQUESTED VARIABLES) ---
    timeNow = datetime.now() # Use timezone-aware datetime if needed for production
    
    # Extract current hour and minute for display/logging
    timeHour = timeNow.hour
    timeMinutes = timeNow.minute
    
    # T_target is the LP budget (activity time only)
    T_target = time_for_activities 
    
    # 1. INITIALIZE AND FILTER DATA (No major changes)
    scheduled_stops = [results[i] for i in path]
    schedulable_periods = [
        item for item in scheduled_stops 
        if item['interestType'] not in ['Start', 'End']
    ]
    N = len(schedulable_periods)

    if N == 0 or T_target <= 0:
        # Fallback for empty or infeasible schedule (simplified for brevity)
        final_schedule = []
        current_time = timeNow
        for i, item in enumerate(scheduled_stops):
            item['scheduled_activity_minutes'] = 0
            item['travel_time_seconds'] = segment_durations[i] if i < len(segment_durations) else 0
            item['arrival_time'] = current_time.strftime("%I:%M %p")
            item['leave_time'] = current_time.strftime("%I:%M %p")
            final_schedule.append(item)
        return final_schedule

    # 2. DATA PROCESSING (No change)
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

    # 3. LINEAR PROGRAMMING MODEL FORMULATION (No change)
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

    # 4. SOLVE AND MAP RESULTS BACK (No change)
    prob.solve()
    final_schedule_map = {}
    if LpStatus[prob.status] == "Optimal":
        for p_id in lp_period_ids:
            final_schedule_map[p_id] = value(x[p_id])
    else:
        for p_id in lp_period_ids:
             final_schedule_map[p_id] = period_data[p_id]["min_duration"]
    
    # 5. CONSTRUCT FINAL OUTPUT WITH ABSOLUTE TIMING
    
    final_schedule = []
    
    # current_arrival_time starts at the actual current time (timeNow)
    current_arrival_time = timeNow 
    
    for i, item in enumerate(scheduled_stops):
        p_id = item['places']['id']
        p_type = item['interestType']
        
        # --- 5A. Determine Activity Time (from LP) ---
        activity_minutes = 0
        if p_type not in ['Start', 'End']:
            activity_minutes = final_schedule_map.get(p_id, 0)
        
        # --- 5B. Calculate Absolute Times ---
        
        # The arrival time at THIS location
        item['arrival_time'] = current_arrival_time.strftime("%I:%M %p")
        
        # The time spent at this stop (0 for Start/End)
        activity_duration_delta = timedelta(minutes=activity_minutes)
        
        # The leave time is Arrival Time + Activity Duration
        leave_time = current_arrival_time + activity_duration_delta
        item['leave_time'] = leave_time.strftime("%I:%M %p")
        
        # --- 5C. Update Accumulator for Next Stop ---
        
        # Travel time FROM this stop TO the next one
        travel_out_seconds = segment_durations[i+1] if i + 1 < len(segment_durations) else 0
        travel_duration_delta = timedelta(seconds=travel_out_seconds)
        
        # The next stop's arrival time is Leave Time + Travel Time Out
        current_arrival_time = leave_time + travel_duration_delta 
        
        # --- 5D. Final Output Formatting ---
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
    print(origin)
    destination = {
        "location": {
            "latLng": {
                "latitude": route[lastIndex]['places']['location']['latitude'],
                "longitude": route[lastIndex]['places']['location']['longitude']
            }
        }
    }
    print(destination)
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
    print(intermediates)
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
     
if __name__ == '__main__':
    app.run(debug=True)