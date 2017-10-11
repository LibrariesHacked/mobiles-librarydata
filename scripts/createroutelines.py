"""Reads all converted authority data and creates route lines to be used in visualisations"""

import csv
import collections
import urllib.request
import pandas as pd
import geopandas
import polyline
import json
from shapely.geometry import Point
from shapely.geometry import LineString

APIKEY = '58d904a497c67e00015b45fcc3d8ff500a48497b5dd7a68a81baf0b2'

def run():
    """Runs the main script"""
    authorities = []
    with open('../data/authorities.csv', 'rt') as authorities_csv:
        reader = csv.reader(authorities_csv, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            authority = row[0]
            code = row[1]
            data = row[4]
            if data != "":
                authorities.append({'code':code, 'filename':data, 'authority':authority})

    authroutes = []
    for auth in authorities:
        routes = {}
        with open('../data/' + auth['filename'], 'rt') as mobilecsv:
            reader = csv.reader(mobilecsv, delimiter=',', quotechar='"')
            next(reader, None)  # skip the headers
            for idx, row in enumerate(reader):
                #[mobile, route, community, stop, address, longitude, latitude, date_output,day, frequency, start, end, timetable])
                mobile = row[0]
                route = row[1]
                community = row[2]
                stop = row[3]
                address = row[4]
                longitude = float(row[5])
                latitude = float(row[6])
                date = row[7]
                day = row[8]
                frequency = row[9]
                start = row[10]
                end = row[11]
                timetable = row[12]
                if route not in routes:
                    routes[route] = collections.OrderedDict()
                point = geopandas.GeoSeries([Point(longitude, latitude)])
                point.crs = {'init' :'epsg:4326'}
                routes[route][idx] = [str(point[0].x), str(point[0].y)]
        authroutes.append({'code':auth['code'], 'authority':auth['authority'], 'routes': routes})

    for auth in authroutes:
        authname = auth['authority']
        auth_geodata = []
        for route in auth['routes']:
            url = 'https://api.openrouteservice.org/directions?api_key=' + APIKEY + '&profile=driving-car&preference=fastest&coordinates='
            for idx,trip in enumerate(routes[route]):
                url = url + routes[route][trip][0] + ',' + routes[route][trip][1] + '|'
            if len(routes[route]) > 1:
                with urllib.request.urlopen(url[:-1]) as response:
                    res_data = json.load(response)
                    line_coords = []
                    for coords in polyline.decode(res_data['routes'][0]['geometry']):
                        line_coords.append(coords[::-1])
                    line = LineString(line_coords)
                    auth_geodata.append({'route': route, 'geo':line})
        frame = pd.DataFrame(data=auth_geodata)
        geo_df = geopandas.GeoDataFrame(frame, crs={'init': 'epsg:4326'}, geometry='geo')
        # Output the route as a GeoJSON format file
        geo_df.to_file('../data/routes/' + authname + '_Routes.geojson', driver="GeoJSON")

run()
