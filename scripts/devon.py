"""Converts raw Devon data to standardised mobile library format"""

import csv
from datetime import datetime
from string import ascii_uppercase

DATA_SOURCE = '../data/devon_raw.csv'
DATA_OUTPUT = '../data/devon.csv'

def run():
    """Runs the main script"""
    mobiles = []
    routes = {}
    char_index = 0

    with open(DATA_SOURCE, 'r') as devon_raw:
        mobreader = csv.reader(devon_raw, delimiter=',', quotechar='"')
        next(mobreader, None)  # skip the headers
        # Mobile,Week,Village,Stop,Arrive,Depart,StartDate,Frequency,Day
        for row in mobreader:
            mobile = row[0].strip()
            week = row[1].strip()
            community = row[2].strip()
            stop = row[3].strip()
            frequency = row[7].strip()
            day = row[8].strip()
            start = row[4].strip()
            end = row[5].strip()
            date = datetime.strptime(row[6].strip(), '%d/%b/%Y')
            timetable = ""
            addr = stop + ', ' + community
            date_output = date.strftime('%Y-%m-%d')

            # We'll make the route number from a combination of mobile, week, and day
            route = mobile + week + day

            mobiles.append(
                [route, community, stop, addr, east, north, date_output,
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
