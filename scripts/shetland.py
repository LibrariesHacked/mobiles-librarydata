"""Converts raw Shetland data to standardised mobile library format"""

import csv
import time
import collections
import urllib.request
from urllib.parse import quote
import json
from datetime import datetime

DATA_SOURCE = '../data/raw/shetland_raw.csv'
DATA_OUTPUT = '../data/shetland.csv'
APIKEY = '58d904a497c67e00015b45fcc3d8ff500a48497b5dd7a68a81baf0b2'

def run():
    """Runs the main script"""
    mobiles = []
    routes = collections.OrderedDict()
    with open(DATA_SOURCE, 'r') as raw:
        mobreader = csv.reader(raw, delimiter=',', quotechar='"')
        next(mobreader, None)
        for row in mobreader:
            # Mobile,Route,Stop,Start,End,Day,Date,Frequency,Timetable
            mobile = row[0].strip()
            route = row[1].strip()
            stop = row[2].strip()
            start = row[3].strip()
            end = row[4].strip()
            day = row[5].strip()
            date = datetime.strptime(row[6].strip(), '%d %b %Y')
            frequency = row[7].strip()
            timetable = row[8].strip()

            address = stop + ', Shetland'

            geo_url = 'https://api.openrouteservice.org/geocoding?api_key=' + APIKEY + '&query=' + quote(address) + '&lang=en&limit=1'
            geo_res = urllib.request.urlopen(geo_url)
            geo_data = json.loads(geo_res.read().decode(geo_res.info().get_param('charset') or 'utf-8'))

            longitude = ''
            latitude = ''
            if len(geo_data['features']) < 0:
                longitude = geo_data['features'][0]['geometry']['coordinates'][0]
                latitude = geo_data['features'][0]['geometry']['coordinates'][1]

            mobile = [
                mobile, route, stop, stop, address, longitude, latitude,
                date.strftime('%Y-%m-%d'), day, frequency, start, end, timetable]

            mobiles.append(mobile)

            time.sleep(2)

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
