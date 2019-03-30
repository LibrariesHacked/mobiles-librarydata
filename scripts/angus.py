import json
import geopandas
from datetime import datetime
from shapely.geometry import Point
import re
import csv

DATA_SOURCE = '../data/raw/angus.geojson'
DATA_OUTPUT = '../data/angus.csv'

def run():

    mobiles = []
    with open(DATA_SOURCE) as data_file:
        data = json.load(data_file)

        features = data['features']
        timetable = 'http://www.angus.gov.uk/sites/angus-cms/files/2018-11/Mobile%20Library%20Route%20Timetable%202018-19.pdf'
        frequency = 2

        for feature in features:
            easting = float(feat['geometry']['coordinates'][0][0])
            northing = float(feat['geometry']['coordinates'][0][1])

            mobile_library = feature['properties']['vehicle']
            day = feature['properties']['day'].rstrip('s')
            village = feature['properties']['location']
            stop = feature['properties']['location']
            start = feature['properties']['time_arrive']
            end = feature['properties']['time_depart']

            latitude = ''
            longitude = ''

            point = geopandas.GeoSeries([Point(easting, northing)])
            point.crs = {'init': 'epsg:27700'}
            point = point.to_crs({'init': 'epsg:4326'})

            longitude = str(point[0].x)
            latitude = str(point[0].y)

            mobile = [
                mobile_library, day_number, village, stop, address, longitude, latitude,
                date_output, day, frequency, start, end, timetable]

            mobiles.append(mobile)

    with open(DATA_OUTPUT, 'w', encoding='utf8', newline='') as out_csv:
        mob_writer = csv.writer(out_csv, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        mob_writer.writerow(
            ['Mobile', 'Route', 'Stop', 'Community', 'Address', 'Longitude', 'Latitude',
             'Date', 'Day', 'Frequency', 'Start', 'End', 'Timetable'])
        for sto in mobiles:
            mob_writer.writerow(
                [sto[0], sto[1], sto[2], sto[3], sto[4], sto[5],
                 sto[6], sto[7], sto[8], sto[9], sto[10], sto[11], sto[12]])


run()
