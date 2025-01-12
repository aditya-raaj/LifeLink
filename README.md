# 🚑 Life Link: Bangalore Closest Ambulance Route Finder

## **Overview**
Life Link is an interactive web application designed to provide real-time assistance during medical emergencies. It identifies the closest available ambulance in Bangalore, calculates the shortest route to the emergency location, and provides an estimated time of arrival (ETA). The app also includes a **First Aid Instructions** feature, offering guidance for small and severe emergencies.

The application uses advanced geospatial and machine learning techniques to ensure accurate location mapping, efficient routing, and timely response.

---

## **Features**
### **1. Closest Ambulance Finder**
- Takes the **emergency address** as input.
- Locates the nearest ambulance based on its geographic coordinates using a **K-Nearest Neighbors (KNN)** model.

### **2. Route Optimization**
- Retrieves the road network of Bangalore from OpenStreetMap using the `osmnx` library.
- Calculates the shortest route from the ambulance to the emergency location using **Dijkstra's shortest path algorithm**.

### **3. Estimated Time of Arrival (ETA)**
- Considers current road congestion levels based on the time of day.
- Dynamically adjusts the speed of the ambulance to provide an accurate ETA.

### **4. Real-Time Map Visualization**
- Displays the shortest route on an interactive **folium map**.
- Highlights the ambulance's starting point and the emergency destination.

### **5. First Aid Instructions**
- Offers essential first aid guidance for both small and severe emergencies.
- Always accessible and persistent throughout the user session.

---

## **Technologies Used**
### **Backend**
- **Python**: Core programming language.
- **Pandas**: Data manipulation for ambulance datasets.
- **NumPy**: Numerical operations for geospatial calculations.
- **scikit-learn**: KNN model for locating the nearest ambulance.
- **osmnx**: Road network extraction and shortest path computation.
- **networkx**: Graph-based analysis for route calculations.

### **Frontend**
- **Streamlit**: Framework for building an interactive and user-friendly web application.
- **folium**: Map visualization for real-time route display.

---

## **How It Works**

### **Input**
1. The user enters the **emergency address** into a text field (e.g., "MG Road").
2. The application geocodes the address to retrieve its latitude and longitude.

### **Processing**
1. **Locate the Nearest Ambulance**:
   - Uses a **KNN model** to find the closest ambulance based on pre-stored latitude and longitude data.
   - Ambulance data is stored in a CSV file (`final_dataset.csv`) with columns:
     - `license_plate`: Unique identifier for the ambulance.
     - `location.latitudes`: Latitude of the ambulance.
     - `location.longitudes`: Longitude of the ambulance.

2. **Shortest Path Calculation**:
   - Extracts the road network of Bangalore using OpenStreetMap data.
   - Computes the shortest route using Dijkstra’s algorithm.

3. **Calculate ETA**:
   - Adjusts ambulance speed dynamically based on the current hour's congestion level.
   - Congestion levels are predefined for each hour of the day.

### **Output**
- **Emergency Location**:
  - Address, latitude, and longitude of the emergency site.
- **Closest Ambulance Information**:
  - License plate, current location, and distance from the emergency site.
- **Estimated Time of Arrival (ETA)**:
  - Displayed in minutes.
- **Route Visualization**:
  - An interactive map showing the shortest route from the ambulance to the emergency location.

---
## Contributors

-  **Aditya Raj** ([GitHub Profile](https://github.com/aditya-raaj))
-  **Mayur** ([GitHub Profile](https://github.com/mayurmk1704))

