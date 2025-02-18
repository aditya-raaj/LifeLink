import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium
from geopy.geocoders import Nominatim
from sklearn.neighbors import NearestNeighbors
import networkx as nx
import osmnx as ox
import datetime
from streamlit_folium import st_folium
from folium.plugins import HeatMap


# Set Streamlit page configuration
st.set_page_config(page_title="🚑 Life Link", page_icon="🚑", layout="wide")

# Set osmnx timeout globally
ox.settings.timeout = 300

# Load ambulance data
df = pd.read_csv("data/final_dataset.csv")  
df1= pd.read_csv("data/dataset1.csv") 

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
    base_speed_kph = 60  # Default speed on uncongested roads in km/h
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

# Sidebar
st.sidebar.title("🚑 Life Link Navigation")
page = st.sidebar.selectbox("", ["Emergency", "Analysis"])

# ----------------------------- Emergency Section ----------------------------- #
if page == "Emergency":
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

# ----------------------------- Analysis Section ----------------------------- #
elif page == "Analysis":
    
    st.title("📊 Bangalore Ambulance Analysis")
    st.subheader("Insights from the Ambulance across Bangalore")
    analysis_type = st.selectbox("Select Analysis Type:", ["Ambulance Distribution", "Clustering for Optimal Placement", "Coverage Radius Visualization","Heatmap Analysis","Ambulance Type Distribution","Service Status Analysis","Traffic Analysis","Traffic Light Visualization"])
    st.write(f"📊 You selected: {analysis_type}")


    # 1. Ambulance Distribution
    if analysis_type == "Ambulance Distribution":
        st.header("Ambulance Distribution Across Bengaluru")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df['location.longitudes'], df['location.latitudes'], c="red", alpha=1, label="Ambulances")
        ax.set_title("Ambulance Distribution")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.legend()
        st.pyplot(fig)

    # 2. Clustering for Optimal Placement
    elif analysis_type == "Clustering for Optimal Placement":
        st.header("Clustering Ambulances for Optimal Placement")
        num_clusters = st.sidebar.slider("Select Number of Clusters", min_value=2, max_value=10, value=5)

        # Perform clustering
        from sklearn.cluster import KMeans
        coords = df[["location.latitudes", "location.longitudes"]].values
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(coords)
        centroids = kmeans.cluster_centers_
        fig, ax = plt.subplots(figsize=(8, 6))
        scatter = ax.scatter(coords[:, 1], coords[:, 0], c=kmeans.labels_, cmap="viridis", alpha=0.6)
        ax.scatter(centroids[:, 1], centroids[:, 0], c="red", marker="x", label="Cluster Centers")
        ax.set_title("Optimal Ambulance Placement")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.legend()
        st.pyplot(fig)

    # 3. Coverage Radius Visualization
    elif analysis_type == "Coverage Radius Visualization":
        st.header("Ambulance Coverage Radius Visualization")
        # Create a folium map
        map_bangalore = folium.Map(location=[12.9716, 77.5946], zoom_start=12)

        # Add ambulances and coverage circles
        for _, row in df.iterrows():
            folium.Marker(
                location=[row["location.latitudes"], row["location.latitudes"]],
                popup=f"Ambulance ID: {row['license_plate']}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(map_bangalore)
            folium.Circle(
                location=[row["location.latitudes"], row["location.longitudes"]],
                radius=5000,  # Example radius in meters
                color="red",
                fill=True,
                fill_opacity=0.3
            ).add_to(map_bangalore)

        # Display the map
        st_data = st_folium(map_bangalore, width=700, height=500)

    elif analysis_type == "Heatmap Analysis":
        st.header("Ambulance Heatmap")

        # Step 1: Remove invalid latitude/longitude
        df_clean = df1[
            (df1["latitude01"] != 0)
            & (df1["longitude01"] != 0)
            & (df1["latitude01"].between(-90, 90))
            & (df1["longitude01"].between(-180, 180))
        ]

        # Step 2: Normalize accident intensity for coloring
        normalized_indices = np.linspace(0, 1, len(df_clean))

        # Step 3: Plot heatmap
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(
            df_clean["longitude01"],
            df_clean["latitude01"],
            alpha=0.5,
            c=normalized_indices,
            cmap="viridis",
            s=50
        )
        plt.colorbar(scatter, label="Accident Intensity")
        plt.title("Heatmap of Ambulance Locations")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        st.pyplot(fig)

    elif analysis_type == "Ambulance Type Distribution":
        st.header("Ambulance Type Distribution")

        # Group by vehicle type
        type_counts = df["emergencyVehicleType"].value_counts()

        # Pie Chart
        fig, ax = plt.subplots()
        ax.pie(
            type_counts,
            labels=type_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["skyblue", "orange"]
        )
        ax.set_title("Vehicle Type Distribution")
        st.pyplot(fig)
    

    elif analysis_type == "Service Status Analysis":
        st.header("Analysis of Ambulances On Duty")

        # Group by ServiceonDuty
        duty_counts = df["serviceOnDuty"].value_counts()

        # Bar Chart
        fig, ax = plt.subplots()
        ax.bar(duty_counts.index, duty_counts.values, color=["green", "red"])
        ax.set_title("Service Status of Ambulances")
        ax.set_xlabel("On Duty Status")
        ax.set_ylabel("Number of Vehicles")
        st.pyplot(fig)

    # 1. Standard Deviation of Travel Times
    elif analysis_type == "Standard Deviation of Travel Times":
        st.header("Standard Deviation of Travel Times Around Bangalore")

        # Filepath to the CSV file
        csv_filepath = "data/traffic_congestion.csv"

        df = pd.read_csv(csv_filepath)

        # Ensure the required columns exist
        if {"Hour", "Std_Dev"}.issubset(df.columns):
            # Convert data types
            df["Hour"] = df["Hour"].astype(int)
            df["Std_Dev"] = df["Std_Dev"].astype(float)

            # Streamlit UI
            st.title("🚦 Traffic Congestion Analysis")
            st.subheader("Standard Deviation of Travel Times Around Bangalore")

            # Create a Matplotlib figure
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Plot Bar Graph
            ax.bar(df["Hour"], df["Std_Dev"], color="skyblue", alpha=1.0, label="Bar Graph")

            # Overlay Line Chart
            ax.plot(df["Hour"], df["Std_Dev"], marker="o", color="red", label="Line Chart", linewidth=2)

            # Customize the plot
            ax.set_title("Standard Deviation of Travel Times Around Bangalore", fontsize=14)
            ax.set_xlabel("Hour of the Day", fontsize=12)
            ax.set_ylabel("Std Dev of Travel Time (mins)", fontsize=12)
            ax.set_xticks(df["Hour"])
            ax.grid(axis="y", linestyle="--", alpha=0.7)
            ax.legend()

            # Show plot in Streamlit
            from PIL import Image

            # Load and display image
            image = Image.open("traffic_data.png")
            st.image(image, caption="Sample Image", use_column_width=True)
    elif analysis_type == "Traffic Light Visualization":
        st.header("Traffic Light Visualization in Bangalore")

        # Load Bengaluru road network
        st.write("Loading road network of Bangalore. This might take a few moments...")
        location = "Bengaluru, Karnataka, India"
        graph = ox.graph_from_place(location, network_type="drive")

        # Extract traffic lights (nodes with 'highway=traffic_signals')
        st.write("Extracting traffic light nodes...")
        traffic_lights = ox.graph_to_gdfs(graph, nodes=True, edges=False)
        traffic_lights = traffic_lights[traffic_lights["highway"] == "traffic_signals"]

        # Create a map to visualize traffic lights
        st.write("Visualizing traffic lights on the map...")
        traffic_map = folium.Map(location=[12.9716, 77.5946], zoom_start=12)

        # Add traffic light markers to the map
        for idx, row in traffic_lights.iterrows():
            folium.Marker(
                location=(row.geometry.y, row.geometry.x),
                popup="Traffic Light",
                icon=folium.Icon(color="red", icon="info-sign"),
            ).add_to(traffic_map)

        # Display the map in Streamlit
        st_folium(traffic_map, width=700, height=500)
