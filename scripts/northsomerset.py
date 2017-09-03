"""Converts raw North Somerset data to standardised mobile library format"""

import csv
from datetime import datetime
from string import ascii_uppercase

DATA_SOURCE = '../data/northsomerset_raw.csv'
DATA_OUTPUT = '../data/northsomerset.csv'

def run():
    """Runs the main script"""
    mobiles = []
    routes = {}
    char_index = 0

    with open(DATA_SOURCE, 'r') as northsom_raw:
        mobreader = csv.reader(northsom_raw, delimiter=',', quotechar='"')
        next(mobreader, None)  # skip the headers
        for row in mobreader:
            com = row[0].strip()
            stop = row[1].strip()
            frequency = row[2].strip().replace('weekly', '1').replace('fortnightly', '2')
            day = row[3].strip()
            time = row[4].strip()
            start = time.split('-')[0].replace('.', ':').strip()
            end = time.split('-')[1].replace('.', ':').strip()
            date = datetime.strptime(row[5].strip(), '%d %b %Y')
            timetable = row[6].strip()
            east = row[7].strip()
            north = row[8].strip()
            addr = stop + ', ' + com
            date_output = date.strftime('%Y-%m-%d')

            # We don't have a route number but need a way of grouping together stops
            if (day + ' ' + date_output) not in routes:
                routes[day + ' ' + date_output] = ascii_uppercase[char_index]
                char_index = char_index + 1

            route = routes[day + ' ' + date_output]

            mobiles.append(
                [route, com, stop, addr, east, north, date_output,
                 day, frequency, start, end, timetable])

    with open(DATA_OUTPUT, 'w', encoding='utf8', newline='') as out_csv:
        mob_writer = csv.writer(out_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        mob_writer.writerow(
            ['Route', 'Stop', 'Community', 'Address', 'Easting', 'Northing',
             'Date', 'Day', 'Frequency', 'Start', 'End', 'Timetable'])
        for sto in mobiles:
            mob_writer.writerow(
                [sto[0], sto[1], sto[2], sto[3], sto[4], sto[5],
                 sto[6], sto[7], sto[8], sto[9], sto[10], sto[11]])
run()
