import urllib.request, json
with urllib.request.urlopen("https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind-1-hour.json") as url:
    data = json.load(url)

    for row in data:
        print(row)

