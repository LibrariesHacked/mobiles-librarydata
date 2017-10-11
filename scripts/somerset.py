"""Converts raw Somerset data to standardised mobile library format"""

import csv
import time
import collections
import urllib.request
import json
from datetime import datetime

DATA_SOURCE = '../data/raw/somerset_raw.csv'
DATA_OUTPUT = '../data/somerset.csv'

def run():
    """Runs the main script"""
    mobiles = []
    routes = collections.OrderedDict()
    with open(DATA_SOURCE, 'r') as som_raw:
        mobreader = csv.reader(som_raw, delimiter=',', quotechar='"')
        next(mobreader, None)
        for row in mobreader:
            stop = row[0].strip()
            community = row[1].strip()
            postcode = row[2].strip()
            start = row[3].strip()
            end = row[4].strip()
            route = row[5].strip()
            date = datetime.strptime(row[6].strip(), '%d/%m/%Y')
            day = row[7].strip()
            frequency = row[8].strip()
            timetable = row[9].strip()

            address = stop + ', ' + community + ', ' + postcode

            pc_url = 'https://api.postcodes.io/postcodes/' + postcode
            pc_rs = urllib.request.urlopen(pc_url)
            pc_data = json.loads(pc_rs.read().decode(pc_rs.info().get_param('charset') or 'utf-8'))

            latitude = pc_data['result']['latitude']
            longitude = pc_data['result']['longitude']

            mobile = [
                'Taunton', route, community, stop, address, longitude, latitude,
                date.strftime('%Y-%m-%d'), day, frequency, start, end, timetable]

            mobiles.append(mobile)

            time.sleep(1)

            if routes.get(route) is None:
                routes[route] = collections.OrderedDict()
            routes[route][stop] = [latitude, longitude]

    with open(DATA_OUTPUT, 'w', encoding='utf8', newline='') as out_csv:
        mob_writer = csv.writer(out_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        mob_writer.writerow(
            ['Mobile', 'Route', 'Community', 'Stop', 'Address', 'Longitude',
             'Latitude', 'Date', 'Day', 'Frequency', 'Start', 'End', 'Timetable'])
        for stop in mobiles:
            mob_writer.writerow(
                [stop[0], stop[1], stop[2], stop[3], stop[4], stop[5], stop[6],
                 stop[7], stop[8], stop[9], stop[10], stop[11], stop[12]])

run()
