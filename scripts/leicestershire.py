"""Converts raw Devon data to standardised mobile library format"""

import csv
import json
import urllib.request
from urllib.parse import quote
from datetime import datetime
import time

DATA_SOURCE = '../data/raw/leicestershire_raw.csv'
DATA_OUTPUT = '../data/leicestershire.csv'
APIKEY = '58d904a497c67e00015b45fcc3d8ff500a48497b5dd7a68a81baf0b2'

def run():
    """Runs the main script"""
    mobiles = []
    with open(DATA_SOURCE, 'r') as raw:
        mobreader = csv.reader(raw, delimiter=',', quotechar='"')
        next(mobreader, None)  # skip the headers
        # Mobile,Route,Community,Stopping Place,From,To,Day,Date,Frequency
        for row in mobreader:
            mobile = row[0].strip()
            route = row[1].strip()
            # We should make the route unique so combine with mobile e.g. A1
            route = mobile + route
            community = row[2].strip()
            stop = row[3].strip()
            start = row[4].strip().replace('.', ':')
            end = row[5].strip().replace('.', ':')
            day = row[6].strip()
            date = datetime.strptime(row[7].strip(), '%d-%b-%Y')
            frequency = row[8].strip()
            timetable = 'https://www.leicestershire.gov.uk/leisure-and-community/libraries/mobile-library-routes'
            address = stop + ', ' + community
            date_output = date.strftime('%Y-%m-%d')
            address_json = {
                "address": stop + ', ' + community,
                "locality": "Leicestershire",
                "country": "EN"
                }

            boundingbox = '-1.59755,52.39215,-0.66411,52.97766'

            geo_url = 'https://api.openrouteservice.org/geocoding?boundary_type=rect&rect=' + boundingbox + '&api_key=' + APIKEY + '&query=' + quote(json.dumps(address_json)) + '&lang=en&limit=1'
            print(geo_url)
            geo_res = urllib.request.urlopen(geo_url)
            geo_data = json.loads(geo_res.read().decode(geo_res.info().get_param('charset') or 'utf-8'))

            longitude = ''
            latitude = ''
            if len(geo_data['features']) > 0:
                longitude = geo_data['features'][0]['geometry']['coordinates'][0]
                latitude = geo_data['features'][0]['geometry']['coordinates'][1]
            else:
                time.sleep(5)
                address_json = {
                    "address": community,
                    "locality": "Leicestershire",
                    "country": "EN"
                }
                geo_url = 'https://api.openrouteservice.org/geocoding?boundary_type=rect&rect=' + boundingbox + '&api_key=' + APIKEY + '&query=' + quote(address) + '&lang=en&limit=1'
                print(geo_url)
                geo_res = urllib.request.urlopen(geo_url)
                geo_data = json.loads(geo_res.read().decode(geo_res.info().get_param('charset') or 'utf-8'))

            if len(geo_data['features']) > 0:
                longitude = geo_data['features'][0]['geometry']['coordinates'][0]
                latitude = geo_data['features'][0]['geometry']['coordinates'][1]

            mobile = [
                mobile, route, community, stop, address, longitude, latitude,
                date_output, day, frequency, start, end, timetable]

            mobiles.append(mobile)

            time.sleep(5)

    with open(DATA_OUTPUT, 'w', encoding='utf8', newline='') as out_csv:
        mob_writer = csv.writer(out_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        mob_writer.writerow(
            ['Mobile', 'Route', 'Community', 'Stop', 'Address', 'Longitude',
             'Latitude', 'Date', 'Day', 'Frequency', 'Start', 'End', 'Timetable'])
        for sto in mobiles:
            mob_writer.writerow(
                [sto[0], sto[1], sto[2], sto[3], sto[4], sto[5],
                 sto[6], sto[7], sto[8], sto[9], sto[10], sto[11], sto[12]])     

run()
