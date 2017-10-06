"""Reads all converted authority data and creates route lines to be used in visualisations"""

import csv
import collections
import urllib

def run():
    """Runs the main script"""
    authorities = []
    with open('../data/authorities.csv', 'rb') as authorities_csv:
        reader = csv.reader(authorities_csv, delimiter=',', quotechar='"')
        next(reader, None)
        for row in reader:
            authority = row[0]
            code = row[1]
            data = row[4]
            
            if data != "":
                authorities.append({ 'code':code, 'filename':data, 'authority':authority })
                
    for auth in authorities:
        with open('../data/' + auth['filename'], 'rb') as mobilecsv:
            reader = csv.reader(mobilecsv, delimiter=',', quotechar='"')
            next(reader, None)  # skip the headers
            routes = collections.OrderedDict()
            for idx, row in reader:
                route = row[0]
                stop = row[1]
                community = row[2]
                address = row[3]
                easting = row[4]
                northing = row[5]
                date = row[6]
                day = row[7]
                frequency = row[8]
                start = row[9]
                end = row[10]
                timetable = row[11]
                if routes.get(route) is None:
                    routes[route][idx] = collections.OrderedDict()
                point = geopandas.GeoSeries([Point(easting, northing)])
                point.crs = {'init' :'epsg:27700'}
                point = world.to_crs({'init': 'epsg:4326'}) 
                routes[route][idx] = [point.x,point.y]

        url = ''
        for route in routes:
            for idx,trip in enumerate(routes[route]):        
                if idx == 0:
                    waypoints = ''
                    url = 'http://openls.geog.uni-heidelberg.de/route?start=' + routes[route][trip][1] + ',' + routes[route][trip][0]
                elif idx == 1:
                    waypoints = routes[route][trip][1] + ',' + routes[route][trip][0]
                elif idx == (len(routes[route]) -1):
                    url = url + '&end=' + routes[route][trip][1] + ',' + routes[route][trip][0] + '&via='
                    url = url + waypoints + '&lang=en&distunit=KM&routepref=Car&weighting=Fastest&avoidAreas=&useTMC=false&noMotorways=false&noTollways=false&noUnpavedroads=false&noSteps=false&noFerries=false&instructions=false'
                    gmlFile = urllib.URLopener()
                    gmlFile.retrieve(url, '../data/' + route + '.xml')
                else:
            waypoints = waypoints + ' ' + routes[route][trip][1] + ',' + routes[route][trip][0]

run()