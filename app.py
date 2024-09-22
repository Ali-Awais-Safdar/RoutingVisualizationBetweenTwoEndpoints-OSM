from flask import Flask, render_template, request, jsonify
import folium
import osmnx as ox
import networkx as nx
import json
import time
import requests

class Geocoder:
    base_url = 'https://nominatim.openstreetmap.org/search'
    results = []

    def fetch(self, address):
        headers = {
            'User-Agent': 'MyGeocoderApp/1.0 (your_email@example.com)'
        }

        params = {
            'q': address,
            'format': 'geocodejson'
        }

        # Make the request
        res = requests.get(url=self.base_url, params=params, headers=headers)
        print('HTTP GET request to URL: %s | Status code: %s' % (res.url, res.status_code))

        if res.status_code == 200:
            print(res.json())
            return res
        else:
            print(f"Request failed with status code {res.status_code}")
            return None

    def parse(self, res):
        if res is None:
            return

        try:
            data = res.json()
            
            # Check if 'features' is present and not empty
            if 'features' in data and len(data['features']) > 0:
                label = json.dumps(data['features'][0]['properties']['geocoding']['label'], indent=2)
                coordinates = json.dumps(data['features'][0]['geometry']['coordinates'], indent=2).replace('\n', '').replace('[', '').replace(']', '').strip()

                # Append data to results
                self.results.append({
                    'address': label,
                    'coordinates': coordinates
                })
            else:
                print("No geocoding results found for this address.")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            print(f"Error parsing response: {e}")
    
    def store_results(self):
        # Write results to file
        with open('results.json', 'w') as f:
            f.write(json.dumps(self.results, indent=2))
    
    def run(self, start_address, end_address):
        addresses = [start_address, end_address]

        # Process each address
        for address in addresses:
            res = self.fetch(address)
            if res is not None:
                self.parse(res)

            # Respect Nominatim rate-limiting policies
            time.sleep(2)
        
        # Store results
        self.store_results()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Route to handle geocoding and route finding
@app.route('/find_route', methods=['POST'])
def find_route():
    start_address = request.form['start']
    end_address = request.form['end']

    geocoder = Geocoder()
    geocoder.run(start_address, end_address)

    # Load the results from the JSON file
    with open('results.json', 'r') as f:
        results = json.load(f)

    if len(results) >= 2:
        start_coords = results[0]['coordinates'].split(',')
        end_coords = results[1]['coordinates'].split(',')

        start_lat_lon = (float(start_coords[1]), float(start_coords[0]))
        end_lat_lon = (float(end_coords[1]), float(end_coords[0]))

        # Use OSMnx to get the graph for the area based on the coordinates
        G = ox.graph_from_point(start_lat_lon, dist=20000, network_type='drive')
        
        start_node = ox.distance.nearest_nodes(G, start_lat_lon[1], start_lat_lon[0])
        end_node = ox.distance.nearest_nodes(G, end_lat_lon[1], end_lat_lon[0])

        # Find the shortest path between the nodes
        route = nx.shortest_path(G, start_node, end_node, weight='length')

        # Create a folium map to visualize the route
        route_map = ox.plot_route_folium(G, route, route_color='blue')

        # Save the map as HTML
        route_map.save('templates/route_map.html')

        # Return the rendered map
        return render_template('route_map.html')

    else:
        return jsonify({'error': 'Could not geocode one or both addresses.'})

if __name__ == '__main__':
    app.run(debug=True)
