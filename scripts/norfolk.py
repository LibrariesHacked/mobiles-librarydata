import csv
import json
import re
import operator
from datetime import datetime

DATA_SOURCE = '../data/raw/norfolk_raw.json'
DATA_OUTPUT = '../data/norfolk.csv'

def run():
    """Runs the main script"""
    mobiles = []
    with open(DATA_SOURCE, 'r') as raw:

        geo_data = json.load(raw)

        for data in geo_data['features']:
            # "STOP_NUMBE":6,"ROUTE_NUMB":"CEN120","STOP_NAME":"POUND LANE SAINSBURYS","DETAILS":"Mobile Library Route Number CEN120 will next visit THORPE ST ANDREW, POUND LANE SAINSBURYS on 30/01/2020 Arrival 18:00 Departure 18:30","Distance":null,"OBJECTID":2,"FID_1":null
            row = data['attributes']
            geometry = data['geometry']
            stop_number = row['STOP_NUMBE']
            route = row['ROUTE_NUMB']
            stop = row['STOP_NAME']
            # Mobile Library Route Number CEN120 will next visit THORPE ST ANDREW, POUND LANE SAINSBURYS on 30/01/2020 Arrival 18:00 Departure 18:30
            details = row['DETAILS']
        
            community = re.search(r'will next visit (.+),', details)[1].capitalize()
            date = datetime.strptime(re.search(r'(\d{2}/\d{2}/\d{4})', details)[0], '%d/%m/%Y')
            date_output = date.strftime('%Y-%m-%d')
            day = date.strftime('%A')
            frequency = 1
            start = re.search(r'Arrival (\d{2}:\d{2})', details)[1]
            end = re.search(r'Departure (\d{2}:\d{2})', details)[1]
            address = stop + ', ' + community
            longitude = geometry['x']
            latitude = geometry['y']

            mobile = [
                'Norfolk', route, community, stop, address, longitude, latitude,
                date_output, day, frequency, start, end, '', stop_number]

            mobiles.append(mobile)

    with open(DATA_OUTPUT, 'w', encoding='utf8', newline='') as out_csv:
        mob_writer = csv.writer(out_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        mob_writer.writerow(
            ['Mobile', 'Route', 'Community', 'Stop', 'Address', 'Longitude',
             'Latitude', 'Date', 'Day', 'Frequency', 'Start', 'End', 'Timetable'])
        for stop in sorted(mobiles, key = operator.itemgetter(1, 13)):
            mob_writer.writerow(
                [stop[0], stop[1], stop[2], stop[3], stop[4], stop[5], stop[6],
                 stop[7], stop[8], stop[9], stop[10], stop[11], stop[12]])

run()
