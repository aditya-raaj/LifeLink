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

## **How to Run the Project**

### **Prerequisites**
Ensure you have the following installed:
- Python 3.x
- Required Python libraries (install using the command below)

```bash
pip install -r requirements.txt
```

### **Running the Application**
1. Clone the repository:
```bash
git clone https://github.com/aditya-raaj/LifeLink.git
```
2. Navigate to the project directory:
```bash
cd LifeLink
```
3. Run the Streamlit application:
```bash
streamlit run app.py
```
4. Enter the emergency location in the input field and get the nearest ambulance details along with the optimized route.

---

## **Dataset**
The dataset used in this project can be accessed here: [IUDX Catalogue Link](#)

(Note: The dataset is not uploaded to GitHub. Please use the provided link to access the data.)

---

## **Contributors**

-  **Aditya Raj** ([GitHub Profile](https://github.com/aditya-raaj))
-  **Mayur** ([GitHub Profile](https://github.com/mayurmk1704))
