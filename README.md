# RoutingVisualizationBetweenTwoEndpoints-OSM

## Overview
This project is a Flask web application that utilizes OpenStreetMap (OSM) data to geocode addresses and find the optimal driving route between them. It integrates various libraries such as OSMnx, NetworkX, and Folium to visualize the route on an interactive map.

## Features
- **Geocoding**: Converts human-readable addresses into geographic coordinates using the Nominatim API.
- **File Input/Output**: Reads addresses from `addresses.txt` and stores the corresponding coordinates in `results.json`.
- **Route Finding**: Calculates the shortest path between two locations using OSM data.
- **Map Visualization**: Displays the route on an interactive map using Folium.

## Technologies Used
- **Python**: The primary programming language for the application.
- **Flask**: A lightweight WSGI web application framework.
- **OSMnx**: A library to work with OpenStreetMap data.
- **NetworkX**: A library for the creation, manipulation, and study of complex networks.
- **Folium**: A library for creating interactive maps.
- **Requests**: For making HTTP requests to the Nominatim API.

## Installation
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```
2. **Install required packages**:
   You can install the necessary libraries using pip:
   ```
   pip install Flask folium osmnx networkx requests scikit-learn
   ```
2. **Run the application**:
   Start the Flask server:
   ```
   python app.py
   ```

## Usage
1. Open your web browser and navigate to `http://127.0.0.1:5000`
2. Enter the starting address and destination address in the form.
3. Click the "Find Route" button.
4. The application will process the addresses, find the optimal route, and display it on an interactive map.

## File Details
- **geoCoder.py**: This file reads addresses from `addresses.txt` and stores the corresponding geographic coordinates in `results.json`.
- **app.py**: This file provides the user interface for entering both starting and ending addresses. The determined optimized route is displayed on an interactive map using Folium.

## Output Example
![alt text](https://github.com/Ali-Awais-Safdar/RoutingVisualizationBetweenTwoEndpoints-OSM/blob/master/output.png)

## Acknowledgments
- **OpenStreetMap** for providing the map data
- **Flask** for the web framework.
- **OSMnx** for the utility to work with OSM data.
- **Folium** for map visualization.


