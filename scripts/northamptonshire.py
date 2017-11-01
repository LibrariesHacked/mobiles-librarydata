import json
import geopandas
from datetime import datetime
from shapely.geometry import Point
import re
import csv
from lxml import etree
from lxml import objectify

DATA_SOURCE = '../data/raw/northamptonshire.xml'
DATA_OUTPUT = '../data/northamptonshire.csv'

def run():

    mobiles = []
    with open(DATA_SOURCE) as data_file:

        tree = objectify.parse(data_file)
        root = tree.getroot()
        mobile_library = 'Northamptonshire'
        timetable = 'http://www.bathnes.gov.uk/services/libraries-and-archives/access-all/mobile-library-routes/mobile-library-route-review'
        frequency = 4

        print(root)
        for item in root.iterchildren():
            
            print(item.get('Details'))
            latitude = ''
            longitude = ''
            address = stop + ' ' + village
            start_matches = re.search(r'(\d{2}.\d{2}).+\d{2}.\d{2}', time)
            end_matches = re.search(r'\d{2}.\d{2}.+(\d{2}.\d{2})', time)
            start = ''
            end = ''
            if start_matches is not None:
                start = start_matches[1].replace('.', ':')
            if end_matches is not None:
                end = end_matches[1].replace('.', ':')
            
            point = geopandas.GeoSeries([Point(easting, northing)])
            point.crs = {'init' :'epsg:27700'}
            point = point.to_crs({'init': 'epsg:4326'})
            longitude = str(point[0].x)
            latitude = str(point[0].y)
            date_output = ''

            mobile = [
                mobile_library, day_number, village, stop, address, longitude, latitude,
                date_output, day, frequency, start, end, timetable]

            mobiles.append(mobile)

    with open(DATA_OUTPUT, 'w', encoding='utf8', newline='') as out_csv:
        mob_writer = csv.writer(out_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        mob_writer.writerow(
            ['Mobile', 'Route', 'Stop', 'Community', 'Address', 'Longitude', 'Latitude',
             'Date', 'Day', 'Frequency', 'Start', 'End', 'Timetable'])
        for sto in mobiles:
            mob_writer.writerow(
                [sto[0], sto[1], sto[2], sto[3], sto[4], sto[5],
                 sto[6], sto[7], sto[8], sto[9], sto[10], sto[11], sto[12]])    
run()
