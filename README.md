# Mobiles. LibraryData.

Project to display mobile library timetables in an interactive live dashboard.

## What is it?



## Supporting technology



## Mobile Library data format

For this project to work, it needs to define a standard format to define the stop details of a mobile library.  Different authorities will have differing ways of describing this data.  

| Column | Description | Example |
| ------ | ----------- | ------- |
| Route | A mobile library typically has a set of routes that it will follow for different days.  This is an identifier for the route. | A |
| Day | The day of the week that the route is driven. | Monday | 
| StartDate | This is a reference date.  Used to determine future dates that the route will occur on, based on the frequency. | 2017-01-09 |
| Frequency | The frequency the route will be repeated.  Has to be a weekly identifier. | 2 |
| Stop | The name of the stop. |  |
| Place | The place the stop is located, normally a village or town name. |  |
| Start | The time the mobile library arrives.  |  |
| End | The time the mobile library leaves. |  |
| X | The x coordinate of the library stop.  This could be longitude or easting. |  |
| Y | The y coordinate of the library stop.  This could be latitude of northing. |  |
| Projection | The geographic projection that the coordinates are provided in.  | 27700 |

## Functionality



## File descriptions



## Build



## Deploy



## Third party licences



## Licences

