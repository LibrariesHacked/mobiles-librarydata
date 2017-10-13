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

def run():
    """Runs the main script"""
    mobiles = []
    with open(DATA_SOURCE, 'r') as raw:
        mobreader = csv.reader(raw, delimiter=',', quotechar='"')
        next(mobreader, None)
        for row in mobreader:
            # Mobile,Route,Stop,Postcode,Start,End,Day,Date,Frequency,Timetable
            mobile = row[0].strip()
            route = row[1].strip()
            stop = row[2].strip()
            postcode = row[3].strip()
            start = row[4].strip()
            end = row[5].strip()
            day = row[6].strip()
            date = datetime.strptime(row[7].strip(), '%d/%m/%Y')
            frequency = row[8].strip()
            timetable = row[9].strip()

            address = stop + ', Shetland'

            pc_url = 'https://api.postcodes.io/postcodes/' + postcode
            pc_rs = urllib.request.urlopen(pc_url)
            pc_data = json.loads(pc_rs.read().decode(pc_rs.info().get_param('charset') or 'utf-8'))

            latitude = pc_data['result']['latitude']
            longitude = pc_data['result']['longitude']

            mobile = [
                mobile, route, stop, stop, address, longitude, latitude,
                date.strftime('%Y-%m-%d'), day, frequency, start, end, timetable]

            mobiles.append(mobile)

            time.sleep(1)

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
