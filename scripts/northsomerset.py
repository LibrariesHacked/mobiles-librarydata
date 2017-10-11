"""Converts raw North Somerset data to standardised mobile library format"""

import csv
import geopandas
from datetime import datetime
from shapely.geometry import Point

DATA_SOURCE = '../data/raw/northsomerset_raw.csv'
DATA_OUTPUT = '../data/northsomerset.csv'

def run():
    """Runs the main script"""
    mobiles = []
    routes = {}

    with open(DATA_SOURCE, 'r') as northsom_raw:
        mobreader = csv.reader(northsom_raw, delimiter=',', quotechar='"')
        next(mobreader, None)  # skip the headers
        for row in mobreader:
            mobile = 'North Somerset'
            route = row[0].strip()
            community = row[1].strip()
            stop = row[2].strip()
            frequency = row[3].strip()
            day = row[4].strip()
            start = row[5].strip()
            end = row[6].strip()
            date = datetime.strptime(row[7].strip(), '%d %b %Y')
            timetable = 'http://www.n-somerset.gov.uk/wp-content/uploads/2015/12/mobile-library-timetable-October-2017-March-2018.pdf'
            easting = float(row[8].strip())
            northing = float(row[9].strip())
            point = geopandas.GeoSeries([Point(easting, northing)])
            point.crs = {'init' :'epsg:27700'}
            point = point.to_crs({'init': 'epsg:4326'})
            longitude = str(point[0].x)
            latitude = str(point[0].y)
            address = stop + ', ' + community
            date_output = date.strftime('%Y-%m-%d')

            mobiles.append(
                [mobile, route, community, stop, address, longitude, latitude, date_output,
                 day, frequency, start, end, timetable])

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
