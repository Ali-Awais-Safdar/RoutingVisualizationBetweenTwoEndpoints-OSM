import requests
import json
import time

class Geocoder:
    base_url = 'https://nominatim.openstreetmap.org/search'
    results = []

    def fetch(self, address):
        headers = {
            'User-Agent': 'MyGeocoderApp/1.0 (your_email@example.com)'  # Use a valid email address
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
    
    def run(self):
        # Load addresses
        addresses = []
        with open('addresses.txt', 'r') as f:
            addresses = f.read().splitlines()

        # Process each address
        for address in addresses:
            res = self.fetch(address)
            if res is not None:
                self.parse(res)

            # Respect Nominatim rate-limiting policies
            time.sleep(2)
        
        # Store results
        self.store_results()

# Main driver
if __name__ == '__main__':
    geocoder = Geocoder()
    geocoder.run()
