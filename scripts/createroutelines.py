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

APIKEY = ''

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
                route = row[0]
                stop = row[1]
                community = row[2]
                address = row[3]
                easting = float(row[4])
                northing = float(row[5])
                date = row[6]
                day = row[7]
                frequency = row[8]
                start = row[9]
                end = row[10]
                timetable = row[11]
                if route not in routes:
                    routes[route] = collections.OrderedDict()
                point = geopandas.GeoSeries([Point(easting, northing)])
                point.crs = {'init' :'epsg:27700'}
                point = point.to_crs({'init': 'epsg:4326'})
                routes[route][idx] = [str(point[0].x), str(point[0].y)]
        authroutes.append({'code':auth['code'], 'authority':auth['authority'], 'routes': routes})

    for auth in authroutes:
        authname = auth['authority']
        auth_geodata = []
        for route in auth['routes']:
            url = 'https://api.openrouteservice.org/directions?api_key=' + APIKEY + '&profile=driving-car&preference=fastest&coordinates='
            for idx,trip in enumerate(routes[route]):
                url = url + routes[route][trip][0] + ',' + routes[route][trip][1] + '|'
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
        geo_df.to_file('../data/' + authname + '_Routes.geojson', driver="GeoJSON")

run()
