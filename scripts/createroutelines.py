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
                
    for a in authorities:
        with open('../data/' + a['filename'], 'rb') as mobilecsv:
            reader = csv.reader(mobilecsv, delimiter=',', quotechar='"')
            next(reader, None)  # skip the headers
            routes = collections.OrderedDict()
            for row in reader:
                library = row[1]
                route = row[2]
                routeId = library + route
                if routes.get(routeId) is None:
                    routes[routeId] = collections.OrderedDict()
                latitude = row[11]
                longitude = row[12]
                id = row[0]
                routes[routeId][id] = [latitude,longitude]

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