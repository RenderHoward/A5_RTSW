Prerequsites:

> Python

> Bottle

> SQLite

Files:

> Source code
```
Persistence.py
RTSW.py
```

> Empty database with schema:

```
SolarDB
```

> Simple testing of web API with browser:
```
'Screenshot from 2024-11-24 18-36-37.png'
'Screenshot from 2024-11-24 19-07-16.png'
'Screenshot from 2024-11-24 19-09-15.png'
````

Design intention 

> Project breaks down into two parts, a persistence layer class named "Store" concerned with SQL queries and commands, and a webby part concerned with pulling upstream data from NOAA web sources, caching it in Store, and serving downstream web requests either from saved data, or freshly pulled from urls in https://services.swpc.noaa.gov/. 

> Web service URLs beginning with "Admin" modify and set up cached access to an escaped NOAA.gov url passed as a parameter to the "addsource" API as shown in `Screenshot from 2024-11-24 19-07-16.png`.

> Once this is accomplished subsequent calls to Web service URLs beginning with "cached" can pull records from persisted storage, and if necessary pull newer records from NOAA.gov site. `Screenshot from 2024-11-24 18-36-37` shows an example of a request to the API named "between" for records from `propagated-solar-wind-1-hour` for times between the given parameters of "start and "end". The third API "bracket" will return the two records just before and after the parameter "timestamp".


Potential Improvements

> As long as downstream clients make requests more frequently than the upstream NOAA site is updated this code will give reliable results, but if a long time passes between requests the tables in Store can develop gaps in them.  A solution to this could be as simple as adding a `cron` job to make minimum of one request for each served stream at standard lowest frequency for each stream. (one per hour or one per day etc.)

> I recognize that the feed creating API under the Admin category is not appropriate for the GET request I have set it to.  PUT or POST I expect are more proper. I only fudged this here as I don't know a simple way to test and capture test result for requests more complicated then browser URL screen shots.
