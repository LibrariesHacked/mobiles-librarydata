"""Converts raw Gloucestershire data to standardised mobile library format"""

import csv
import json
import urllib.request
from urllib.parse import quote
from datetime import datetime
import time

DATA_SOURCE = '../data/raw/gloucestershire_raw.csv'
DATA_OUTPUT = '../data/gloucestershire.csv'
APIKEY = '58d904a497c67e00015b45fcc3d8ff500a48497b5dd7a68a81baf0b2'

def run():
    """Runs the main script"""
    mobiles = []
    with open(DATA_SOURCE, 'r') as raw:
        mobreader = csv.reader(raw, delimiter=',', quotechar='"')
        next(mobreader, None)  # skip the headers
        # Week,Day,Route,Village,Stop Name,StartTime,EndTime,Date
        for row in mobreader:

            # Read all the data from the raw spreadsheet
            week = row[0].strip()
            day = row[1].strip()
            route = row[2].strip()
            community = row[3].strip()
            stop = row[4].strip()
            start = row[5].strip()
            end = row[6].strip()
            date = datetime.strptime(row[7].strip(), '%d/%m/%Y')

            frequency = '4'
            mobile = 'Gloucestershire'
            address = stop + ', ' + community
            date_output = date.strftime('%Y-%m-%d')
            timetable = 'http://www.gloucestershire.gov.uk/libraries/find-a-library/mobile-library-service/'

            extent = '-2.68754,51.57754,-1.61520,52.11258'

            address = stop + ' ' + community

            geo_url = 'https://api.openrouteservice.org/geocoding?boundary_type=rect&rect=' + extent + '&api_key=' + APIKEY + '&query=' + quote(address) + '&lang=en&limit=1'
            print(geo_url)
            geo_res = urllib.request.urlopen(geo_url)
            geo_data = json.loads(geo_res.read().decode(geo_res.info().get_param('charset') or 'utf-8'))

            longitude = ''
            latitude = ''
            if len(geo_data['features']) > 0:
                longitude = geo_data['features'][0]['geometry']['coordinates'][0]
                latitude = geo_data['features'][0]['geometry']['coordinates'][1]
            else:
                time.sleep(4)
                address = community
                geo_url = 'https://api.openrouteservice.org/geocoding?boundary_type=rect&rect=' + extent + '&api_key=' + APIKEY + '&query=' + quote(address) + '&lang=en&limit=1'
                print(geo_url)
                geo_res = urllib.request.urlopen(geo_url)
                geo_data = json.loads(geo_res.read().decode(geo_res.info().get_param('charset') or 'utf-8'))

            if len(geo_data['features']) > 0:
                longitude = geo_data['features'][0]['geometry']['coordinates'][0]
                latitude = geo_data['features'][0]['geometry']['coordinates'][1]

            # We'll make the route number from a combination of week and route letter
            route = week + route

            mobile = [
                mobile, route, community, stop, address, longitude, latitude,
                date_output, day, frequency, start, end, timetable]

            mobiles.append(mobile)

            time.sleep(4)

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
