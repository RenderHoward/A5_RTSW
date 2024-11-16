import urllib.request, json
import Persistance

urlstr = "https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind-1-hour.json"

with urllib.request.urlopen(urlstr) as urlstr:
    data = json.load(urlstr)

    store = Persistance.Store("SolarDB", "SolarWind")

    store.begintrans()

    for row in data:
        store.addrecord(row)

    store.endtrans()

