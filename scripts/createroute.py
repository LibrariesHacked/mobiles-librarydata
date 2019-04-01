import csv
import collections
import urllib.request
import pandas as pd
import geopandas
import json
import time
from shapely.geometry import Point
from shapely.geometry import LineString

API_KEY = ''
STOP_DATA = '../data/aberdeenshire.csv'
OUTPUT_DATA = '../data/aberdeenshire_routes.geojson'


def run():
    """Runs the main script"""

    routes = {}
    geodata = []
    with open(STOP_DATA, 'rt') as mobile_csv:

        reader = csv.reader(mobile_csv, delimiter=',', quotechar='"')
        next(reader, None)  # skip the headers
        # make sure the rows are sorted by mobile, route, and arrival time
        sorted_rows = sorted(reader, key=lambda row: (row[1], row[2], row[10]))

        for (idx, row) in enumerate(sorted_rows):

            mobile = row[1]
            route = row[2]
            longitude = float(row[7])
            latitude = float(row[8])

            # Add to object
            if route not in routes:
                # Create an ordered dictionary so we keep track of stop order
                routes[route] = collections.OrderedDict()

            routes[route][idx] = {
                'longitude': str(longitude),
                'latitude': str(latitude)
            }

    for route in routes:

        # construct the URL from the stops
        url = 'https://api.openrouteservice.org/directions?format=geojson&api_key=' + \
            API_KEY + '&profile=driving-car&preference=fastest&coordinates='
        for (idx, trip) in enumerate(routes[route]):
            url = url + routes[route][trip]['longitude'] + \
                ',' + routes[route][trip]['latitude'] + '|'

        # only continue if there is more than one stop
        if len(routes[route]) > 1:
            with urllib.request.urlopen(url[:-1]) as response:
                res_data = json.load(response)
                print(res_data['features'][0]['geometry']['coordinates'])
                line = LineString(res_data['features'][0]['geometry']['coordinates'])
                geodata.append({'route': route, 'geo': line})
                time.sleep(5)

    frame = pd.DataFrame(data=geodata)
    geodf = geopandas.GeoDataFrame(
        frame, crs={'init': 'epsg:4326'}, geometry='geo')

    # output route as geojson format file
    geodf.to_file(OUTPUT_DATA, driver="GeoJSON")

run()
