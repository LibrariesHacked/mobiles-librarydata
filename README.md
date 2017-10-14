Mobiles. LibraryData
====================

Project to display mobile library timetables in an interactive dashboard.

What is it?
-----------

This project takes mobile library schedules from UK public library authorities, and attempts to standardise them into a single format. This can then be used to provide web functionality such a mobile library finder, route visualisations, and live timetable notifications. In future it could also generate digital calendars (e.g. in ICalendar format), or provide notifications for subscribed users.

Mobile Library data format
--------------------------

For this project to work, it needs to define a standard to define the mobile library schedule. Different authorities will have differing ways of describing this data. This standard is likely to change as new services introduce complexities that the original data format cannot hold.

| Column | Description | Example |
| ------ | ----------- | ------- |
| Mobile | A library service may have multiple mobile libraries. For example, Devon have 4, which cover different areas of the county. Sometimes these may have descriptive names, other times letters or numbers. | Tiverton |
| Route | A mobile library typically has a set of routes that groups together the stops it visits within a single day. This is an identifier for the route. This should be a unique value across different mobiles. | A |
| Day | The day of the week that the route is driven. Perhaps not required given that we will also have a date value. | Monday | 
| StartDate | This is a reference date. One is required. It is used to determine future dates that the route will occur on, based upon the frequency. | 2017-01-09 |
| Frequency | The frequency the route will be repeated. Currently an integer to represent a week. For example 2 would mean the mobile library route repeats every 2 weeks. However, some mobile library services are in the form 'every first thursday of the month'.  How do we deal with that? | 2 |
| Stop | The name of the stop. Normally a decriptive location or address.  | Opposite the willow tree |
| Community | The place the stop is located, Normally a village or town name. | Kerswell |
| Start | The time the mobile library arrives. | 15:30 |
| End | The time the mobile library leaves. | 16:00 |
| X | The x coordinate of the library stop. This should be the longitude based upon WGS84 coordinates. |  |
| Y | The y coordinate of the library stop.  This should be the latitude based upon WGS24 coordinates. |  |

Licence
-------

Original code licensed under the MIT Licence.
