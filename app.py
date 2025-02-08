import streamlit as st
import pandas as pd
import numpy as np
import folium
from geopy.geocoders import Nominatim
from sklearn.neighbors import NearestNeighbors
import networkx as nx
import osmnx as ox
import datetime
from streamlit_folium import st_folium

# Set Streamlit page configuration
st.set_page_config(page_title="🚑 Life Link", page_icon="🚑", layout="centered")

# Set osmnx timeout globally
ox.settings.timeout = 300

# Load ambulance data
df = pd.read_csv("data/final_dataset.csv")  

# Prepare KNN model for ambulance locations
ambulance_coords = df[["location.latitudes", "location.longitudes"]].values
knn = NearestNeighbors(n_neighbors=1, algorithm="ball_tree", metric="haversine")
knn.fit(np.radians(ambulance_coords))

# Congestion levels for each hour of the day
hourly_congestion_levels = {
    0: 6, 1: 6.6, 2: 6.25, 3: 6.4, 4: 6.6, 5: 6.2, 6: 6.5, 7: 8.25, 8: 9.8, 9: 10.75, 10: 9.75,
    11: 9, 12: 8.75, 13: 9, 14: 8.8, 15: 9.2, 16: 10, 17: 11, 18: 11.75, 19: 10.3, 20: 8.5,
    21: 7.25, 22: 7, 23: 6.5
}

# Function to calculate average speed based on congestion level
def calculate_speed(congestion_level):
    base_speed_kph = 120  # Default speed on uncongested roads in km/h
    adjusted_speed_kph = base_speed_kph * (congestion_level / 12)
    return max(5, adjusted_speed_kph)  # Ensure speed doesn't drop below 5 km/h

# Function to get current congestion level
def get_congestion_level():
    current_hour = datetime.datetime.now().hour
    return hourly_congestion_levels[current_hour]

# Initialize session state for results, map, and first aid instructions
if "map" not in st.session_state:
    st.session_state["map"] = None
if "results" not in st.session_state:
    st.session_state["results"] = None
if "first_aid_shown" not in st.session_state:
    st.session_state["first_aid_shown"] = False

# Streamlit UI
st.title("🚑 Life Link")
st.subheader("Bangalore Closest Ambulance Route Finder")

# Input: Emergency Address
emergency_address = st.text_input("Enter Emergency Address:", placeholder="e.g., MG Road")

if st.button("Find Closest Ambulance"):
    if emergency_address:
        # Geocode the emergency location
        geolocator = Nominatim(user_agent="geoapi")
        emergency_location = geolocator.geocode(f"{emergency_address}, Bangalore, Karnataka")

        if emergency_location:
            # Extract emergency location details
            latitude_degrees = emergency_location.latitude
            longitude_degrees = emergency_location.longitude

            # Predict closest ambulance
            emergency_coords = np.radians([[latitude_degrees, longitude_degrees]])
            distances, indices = knn.kneighbors(emergency_coords)
            closest_ambulance_index = indices[0][0]
            closest_ambulance = df.iloc[closest_ambulance_index]

            # Load the road network
            location = "Bengaluru, Karnataka, India"
            graph = ox.graph_from_place(location, network_type="drive")
            graph = ox.distance.add_edge_lengths(graph)

            # Define origin (ambulance location) and destination (emergency location)
            orig_point = (closest_ambulance['location.latitudes'], closest_ambulance['location.longitudes'])
            dest_point = (latitude_degrees, longitude_degrees)

            # Find nearest nodes and shortest route
            orig_node = ox.nearest_nodes(graph, orig_point[1], orig_point[0])  # OSM expects (lon, lat)
            dest_node = ox.nearest_nodes(graph, dest_point[1], dest_point[0])
            route = nx.shortest_path(graph, orig_node, dest_node, weight="length")

            # Route coordinates for visualization
            route_coords = [(graph.nodes[node]["y"], graph.nodes[node]["x"]) for node in route]

            # Calculate ETA
            congestion_level = get_congestion_level()
            average_speed_kph = calculate_speed(congestion_level)
            average_speed_mps = average_speed_kph * 1000 / 3600

            route_length = sum(graph[u][v][0]["length"] for u, v in zip(route[:-1], route[1:]))
            travel_time_seconds = route_length / average_speed_mps

            # Prepare results
            total_eta_minutes = travel_time_seconds / 60
            results = {
                "emergency_address": emergency_address,
                "emergency_location": (latitude_degrees, longitude_degrees),
                "ambulance_info": {
                    "license_plate": closest_ambulance["license_plate"],
                    "location": (closest_ambulance["location.latitudes"], closest_ambulance["location.longitudes"]),
                    "distance": distances[0][0] * 6371,
                },
                "eta": total_eta_minutes,
            }

            # Visualize the route on a map
            route_map = folium.Map(location=orig_point, zoom_start=12)
            folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(route_map)
            folium.Marker(orig_point, popup="Ambulance", icon=folium.Icon(color="green")).add_to(route_map)
            folium.Marker(dest_point, popup="Emergency", icon=folium.Icon(color="red")).add_to(route_map)

            # Save results and map in session state
            st.session_state["results"] = results
            st.session_state["map"] = route_map
        else:
            st.error("Location not found. Please try again.")

# Display the map if available in session state
if st.session_state["map"]:
    st_folium(st.session_state["map"], width=700, height=500)

# Display results if available in session state
if st.session_state["results"]:
    results = st.session_state["results"]
    st.write("### Emergency Details")
    st.write(f"- **Address**: {results['emergency_address']}")
    st.write(f"- **Location**: Latitude {results['emergency_location'][0]}, Longitude {results['emergency_location'][1]}")
    st.write(f"### Closest Ambulance")
    st.write(f"- **License Plate**: {results['ambulance_info']['license_plate']}")
    st.write(f"- **Location**: Latitude {results['ambulance_info']['location'][0]}, Longitude {results['ambulance_info']['location'][1]}")
    st.write(f"- **Distance to Emergency**: {results['ambulance_info']['distance']:.2f} km")
    st.write(f"### Estimated Time of Arrival (ETA)")
    st.write(f"- **ETA**: {results['eta']:.2f} minutes")

# Persistent First Aid Instructions
if st.button("First Aid Instructions") or st.session_state["first_aid_shown"]:
    st.session_state["first_aid_shown"] = True
    st.header("🩹 First Aid Instructions") 

    st.markdown("""
    **1. Small Emergencies** 
        -  Clean the wound with soap and water.
        -  Apply gentle pressure with a clean cloth to stop bleeding. 
        -  Cover the wound with a clean bandage.

    **2. Severe Emergencies**
        - **Call for Immediate Help:** Dial 102 (or your local emergency number).   
        - **Check for Responsiveness:** Shout and gently shake the person.     
        - **Check for Breathing:** Look, listen, and feel for breath.  
        - **If not breathing:** Begin CPR (if trained). 
        - **Control Bleeding:** Apply direct pressure to any severe bleeding. 
        - **Prevent Shock:** Keep the patient warm and elevate their legs slightly (if possible).
        - **Stay with the Patient:** Reassure them and monitor their condition until help arrives.
    """)