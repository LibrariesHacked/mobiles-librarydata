import json
import csv
from datetime import datetime

# The original raw data for Aberdeenshire is web JSON data
DATA_SOURCE = '../data/raw/aberdeenshire.json'
DATA_OUTPUT = '../data/aberdeenshire.csv'

def run():

    mobiles = []
    with open(DATA_SOURCE, encoding='utf-8') as data_file:
	
        mobiles_data = json.load(data_file)

        for mobile in mobiles_data:

            mobile_library = mobile[2].replace('Mobile', '').replace('Library', '').strip()
            timetable = 'https://www.livelifeaberdeenshire.org.uk/media/'
            if "North" in mobile_library:
                timetable = timetable + '2808/mobile-north-timetable-160119.pdf'
            if "Central" in mobile_library:
                timetable = timetable + '2807/mobile-central-timetable-160119.pdf'
            if "South" in mobile_library:
                timetable = timetable + '2809/mobile-south-timetable-160119.pdf'

            # the stops are in an array
            stops = mobile[12][0][13][0]

            for stop in stops:
                coord_y = stop[1][0][0][0]
                coord_x = stop[1][0][0][1]

                stop_name = stop[5][0][1][0].replace('\n','')

                # Attributes are in another array
                day = ''
                start = ''
                end = ''
                week = ''
                dates = ''

                for attr in stop[5][3]:
                    key = attr[0]
                    val = attr[1][0].replace('\n','').strip()
                    if key == 'Day':
                        day = val
                    if key == 'Arrival':
                        start = val
                    if key == 'Departure':
                        end = val
                    if key == 'Week':
                        week = val
                    if key == 'Dates':
                        dates = val

                date_output = ''
                if (dates != '' and len(dates.split(',')) > 0): 
                    date = dates.split(',')[0] + ' 2019' # e.g. January 22 should be 2019-01-22
                    date = datetime.strptime(date, '%B %d %Y')
                    date_output = date.strftime('%Y-%m-%d')

                # calculated fields
                route = week + ' ' + day

                stop_array = stop_name.split(' - ')
                community = stop_array[0]
                stop_name = ''
                if len(stop_array) > 1:
                    stop_name = stop_array[1]
                address = stop_name + ', ' + community

                mobiles.append(
                    [mobile_library, route, community, stop_name, address, 
                    coord_x, coord_y, date_output, day, 2, start, end, timetable]
                )

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