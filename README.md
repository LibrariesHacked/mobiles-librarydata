Mobiles. LibraryData
====================

Project to display mobile library timetables in an interactive live dashboard.

What is it?
-----------

This project takes mobile library data (timetables) from UK public library authorities and attempts to standardise them into a single format.  This can then be used to provide functionality like a mobile library finder, route line visualisations, and live timetable notifications.  In future it could also integrate generating calendars (e.g. in ical format).

Mobile Library data format
--------------------------

For this project to work, it needs to define a standard format to define the mobile library timetable for a library service.  Different authorities will have differing ways of describing this data. This standard is likely to have to change as new services introduce complexities that the original data format cannot hold.

| Column | Description | Example |
| ------ | ----------- | ------- |
| Mobile | A library service may have multiple mobile libraries. For example, Devon have 4, which cover different areas of the county | Tiverton |
| Route | A mobile library typically has a set of routes that it will follow for different days.  This is an identifier for the route. | A |
| Day | The day of the week that the route is driven. | Monday | 
| StartDate | This is a reference date.  Used to determine future dates that the route will occur on, based on the frequency. | 2017-01-09 |
| Frequency | The frequency the route will be repeated. Currently an integer to represent a week.  For example 2 would mean the mobile library route repeats every 2 weeks. However, some mobile library services are in the form 'every first thursday of the month'.  How do we deal with that? | 2 |
| Stop | The name of the stop. Normally a decriptive location or address.  | Opposite the willow tree |
| Community | The place the stop is located, normally a village or town name. | Kerswell |
| Start | The time the mobile library arrives.  | 15:30 |
| End | The time the mobile library leaves. | 16:00 |
| X | The x coordinate of the library stop.  This should be the longitude with coordinate reference 4326. |  |
| Y | The y coordinate of the library stop.  This should be the latitude with coordinate reference 4326. |  |

Licence
-------

Original code licensed under the MIT Licence.
