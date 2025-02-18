# 🚑 Life Link: Bangalore Closest Ambulance Route Finder

## **Overview**
Life Link is an interactive web application designed to provide real-time assistance during medical emergencies. It identifies the closest available ambulance in Bangalore, calculates the shortest route to the emergency location, and provides an estimated time of arrival (ETA). Additionally, the app includes a **First Aid Instructions** feature, offering guidance for minor and severe emergencies.

The application leverages advanced geospatial and machine learning techniques to ensure accurate location mapping, efficient routing, and timely response.

---

## **Features**
### **1. Closest Ambulance Finder**
- Takes the **emergency address** as input.
- Locates the nearest ambulance using a **K-Nearest Neighbors (KNN)** model based on geographic coordinates.

### **2. Route Optimization**
- Retrieves the road network of Bangalore from OpenStreetMap using the `osmnx` library.
- Computes the shortest route using **Dijkstra's shortest path algorithm**.

### **3. Estimated Time of Arrival (ETA)**
- Accounts for real-time road congestion based on the time of day.
- Dynamically adjusts the ambulance's speed to provide an accurate ETA.

### **4. Real-Time Map Visualization**
- Displays the shortest route on an interactive **folium map**.
- Highlights both the ambulance’s starting point and the emergency destination.

### **5. First Aid Instructions**
- Provides essential first aid guidance for various medical emergencies.
- Available throughout the user session for quick reference.

---

## **Technologies Used**
### **Backend**
- **Python**: Core programming language.
- **Pandas**: Data manipulation for ambulance datasets.
- **NumPy**: Numerical operations for geospatial calculations.
- **scikit-learn**: KNN model for nearest ambulance detection.
- **osmnx**: Road network extraction and shortest path computation.
- **networkx**: Graph-based analysis for route calculations.

### **Frontend**
- **Streamlit**: Framework for building an interactive and user-friendly web application.
- **folium**: Map visualization for real-time route display.

---

## **How It Works**

### **Step 1: User Input**
- The user enters the **emergency address** into a text field (e.g., "MG Road").
- The application geocodes the address to retrieve its latitude and longitude.

### **Step 2: Processing**
1. **Locate the Nearest Ambulance**:
   - Utilizes a **KNN model** to find the closest ambulance based on pre-stored location data.
   - Ambulance data is stored in a CSV file (`final_dataset.csv`) containing:
     - `license_plate`: Unique identifier for each ambulance.
     - `location.latitudes`: Latitude of the ambulance.
     - `location.longitudes`: Longitude of the ambulance.

2. **Shortest Path Calculation**:
   - Extracts the road network of Bangalore using OpenStreetMap data.
   - Computes the shortest route using Dijkstra’s algorithm.

3. **Calculate ETA**:
   - Adjusts ambulance speed dynamically based on the current hour's congestion level.
   - Congestion levels are predefined for different times of the day.

### **Step 3: Output**
- **Emergency Location**:
  - Displays address, latitude, and longitude of the emergency site.
- **Closest Ambulance Information**:
  - Shows license plate, current location, and distance from the emergency site.
- **Estimated Time of Arrival (ETA)**:
  - Displayed in minutes.
- **Route Visualization**:
  - An interactive map displaying the shortest route from the ambulance to the emergency location.

---

## **Dataset**
The dataset used in this project can be accessed here: https://catalogue.cos.iudx.org.in/
---

## **Contributors**

-  **Aditya Raj** ([GitHub Profile](https://github.com/aditya-raaj))
-  **Mayur** ([GitHub Profile](https://github.com/mayurmk1704))
