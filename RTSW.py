import urllib.request, json
import Persistance




with urllib.request.urlopen("https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind-1-hour.json") as url:
    data = json.load(url)

    store = Persistance.Store("SolarDB", "SolarWind")

    store.begintrans()

    for row in data:
        store.addrecord(row)

    store.endtrans()

