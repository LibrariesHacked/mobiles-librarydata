import csv
import pandas
from datetime import datetime

mobiles = []
with open('../data/northsomerset_raw.csv', 'r') as northsom_raw:
    mobreader = csv.reader(northsom_raw, delimiter=',', quotechar='"')
    next(mobreader, None)  # skip the headers
    for row in mobreader:
        community = row[0].strip()
        stop = row[1].strip()
        frequency = row[2].strip()
        day = row[3].strip()
        time = row[4].strip()
        start = time.split('-')[0].strip()
        end = time.split('-')[1].strip()
        date = datetime.strptime(row[5].strip(), '%d %b %Y')
        timetable = row[6].strip()
        easting = row[7].strip()
        northing = row[8].strip()
        mobiles.append([community, stop, '', easting, northing, date.strftime('%Y-%m-%d'), day, frequency, start, end, timetable])

with open('../data/northsomerset.csv', 'w', encoding='utf8', newline='') as northsomerset_csv:
    mob_writer = csv.writer(northsomerset_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    mob_writer.writerow(['Route', 'Stop', 'Community', 'Address', 'Easting', 'Northing', 'Date', 'Day', 'Frequency', 'Start', 'End', 'Timetable'])
    for stop in mobiles:
        mob_writer.writerow([stop[0], stop[1], stop[2], stop[3], stop[4], stop[5], stop[6], stop[7], stop[8], stop[9], stop[10]])
