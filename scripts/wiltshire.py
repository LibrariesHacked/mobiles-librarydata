"""Web scrapes Wiltshire Mobile Library Timetables and geocodes them """

from urllib.parse import quote
from datetime import datetime
import json
import os
import csv
import time
import requests
import pyproj
from bs4 import BeautifulSoup

# Open route service API key
APIKEY = '58d904a497c67e00015b45fcc3d8ff500a48497b5dd7a68a81baf0b2'
# Initial file from web scraping
DATA_OUTPUT_RAW = '../data/raw/wiltshire_raw.csv'
# Final file to output
DATA_OUTPUT_FINAL = '../data/wiltshire.csv'
# Wiltshire County bounding box coordinates for geocoding
BBOX = '-2.3656,50.945,-1.4857,51.7031'

def run():
    """Runs the main script"""

    # Scrape stop information. This is a single web page listing stops
    stop_list = 'http://services.wiltshire.gov.uk/MobileLibrary/Library/StopList'
    stop_list_html = requests.get(stop_list)
    stop_list_soup = BeautifulSoup(stop_list_html.text, 'html.parser')

    # If we don't already have it, create the raw file
    if not os.path.isfile(DATA_OUTPUT_RAW):
        mobiles = []
        # For each stop get the stop details
        for link in stop_list_soup.find_all('a'):
            # Detect whether the link is a link to a stop
            if '/MobileLibrary/Library/Stop/' in link.get('href'):

                # Get the webpage
                stop_url = 'http://services.wiltshire.gov.uk' + link.get('href')
                print(stop_url)
                stop_html = requests.get(stop_url)
                stop_soup = BeautifulSoup(stop_html.text, 'html.parser')

                # General stop information
                stop_name = stop_soup.find('h2').text
                community = stop_name.split(', ')[0]
                stop_name = stop_name.split(', ')[1]
                address = stop_name + ', ' + community
                # There are some stops that are two weekly but they're part of separate routes.  Keep them separate
                frequency = 4

                # Detailed information for the stop is found in the table.
                table = stop_soup.find('table').find('tbody')
                stop_rows = table.find_all('tr')

                for stop in stop_rows:
                    round_name = stop.find('a').text.replace('\r\n', '').replace(' (fortnightly stop)', '')
                    mobile_library = round_name.split(', ')[0].replace(' mobile library', '')
                    day_week = round_name.split(', ')[1]
                    route = day_week.replace('week', 'Week')
                    week = day_week.split(' week ')[1]
                    day = day_week.split(' week ')[0]
                    date = datetime.strptime(
                    stop.find('li').text, '%A %d %B, %Y')
                    date_output = date.strftime('%Y-%m-%d')
                    start = stop.find_all('td')[1].text
                    end = stop.find_all('td')[2].text
                    timetable = 'http://services.wiltshire.gov.uk' + stop.find('a').get('href')

                    # Mobile,Route,Stop,Community,Address,Longitude,Latitude,Date,Day,Frequency,Start,End,Timetable
                    mobile = {
                        'mobile': mobile_library, 'route': route,
                        'stop': stop_name, 'community': community, 'address': address, 
                        'date': date_output, 'day': day, 'frequency': frequency,
                        'start': start, 'end': end, 'timetable': timetable
                    }
                    mobiles.append(mobile)
                time.sleep(5)

        with open(DATA_OUTPUT_RAW, 'w', encoding='utf8', newline='') as out_raw:
            mob_writer = csv.writer(
                out_raw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            mob_writer.writerow(
                [
                  'Mobile', 'Route', 'Community', 'Stop', 'Address', 'Date',
                  'Day', 'Frequency', 'Start', 'End', 'Timetable'
                ]
            )
            for sto in mobiles:
                mob_writer.writerow(
                    [
                        sto['mobile'], sto['route'], sto['community'], sto['stop'], sto['address'], sto['date'],
                        sto['day'], sto['frequency'], sto['start'], sto['end'], sto['timetable']
                    ])

    mobiles = []
    with open(DATA_OUTPUT_RAW, 'r', encoding='utf8', newline='') as raw:
        mobreader = csv.reader(raw, delimiter=',', quotechar='"')
        next(mobreader, None)  # skip the headers
        # Mobile,Route,Community,Stop,Address,Date,Day,Frequency,Start,End,Timetable
        for row in mobreader:
            # Initial geocoding URL - use just the community to try to get the right area
            geo_url = (
                'https://api.openrouteservice.org/geocoding?boundary_type=rect&rect=' + BBOX +
                '&api_key=' + APIKEY + '&query=' + quote(row[2]) + '&limit=1')
            print(geo_url)

            attempts = 0
            while attempts < 100:
                try:
                    time.sleep(10)
                    geo_res = requests.get(geo_url)
                    geo_data = json.loads(geo_res.content)
                    break
                except:
                    attempts += 1

            longitude = ''
            latitude = ''
            if len(geo_data['features']) > 0:
                longitude = geo_data['features'][0]['geometry']['coordinates'][0]
                latitude = geo_data['features'][0]['geometry']['coordinates'][1]

            # Now, geocode again, this time with the extra detail
            geo_url = (
                'https://api.openrouteservice.org/geocoding?boundary_type=rect&rect=' +
                BBOX + '&api_key=' + APIKEY + '&query=' +
                quote(row[4]) + '&lang=en&limit=1')
            print(geo_url)

            attempts = 0
            while attempts < 100:
                try:
                    time.sleep(10)
                    geo_res = requests.get(geo_url)
                    geo_data = json.loads(geo_res.content)
                    break
                except:
                    attempts += 1

            if len(geo_data['features']) > 0:
                lng = geo_data['features'][0]['geometry']['coordinates'][0]
                lat = geo_data['features'][0]['geometry']['coordinates'][1]
                geod = pyproj.Geod(ellps='WGS84')
                angle1, angle2, distance = geod.inv(lng, lat, longitude, latitude)

                # Only set the new latitude and longitude IF it's within 2 miles of the original
                if distance < 3218:
                    longitude = lng
                    latitude = lat

            # Mobile,Route,Stop,Community,Address,Longitude,Latitude,Date,Day,Frequency,Start,End,Timetable
            mobile = {
                'mobile': row[0], 'route': row[1],
                'stop': row[2], 'community': row[3], 'address': row[4], 'longitude': longitude,
                'latitude': latitude, 'date': row[5], 'day': row[6], 'frequency': row[7],
                'start': row[8], 'end': row[9], 'timetable': row[10]
            }
            mobiles.append(mobile)

    with open(DATA_OUTPUT_FINAL, 'w', encoding='utf8', newline='') as out:
        mob_writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        mob_writer.writerow(
            [
                'Mobile', 'Route', 'Community', 'Stop', 'Address', 'Longitude',
                'Latitude', 'Date', 'Day', 'Frequency', 'Start', 'End', 'Timetable'])
        for sto in mobiles:
            mob_writer.writerow(
                [
                    sto['mobile'], sto['route'], sto['community'], sto['stop'], sto['address'],
                    sto['longitude'], sto['latitude'], sto['date'], sto['day'], sto['frequency'],
                    sto['start'], sto['end'], sto['timetable']
                ])

run()
