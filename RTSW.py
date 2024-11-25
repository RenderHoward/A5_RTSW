import urllib.request, json
import Persistence

def bracket( tbl, timestamp ) -> []:
    store = Persistence.Store("SolarDB", tbl)

    if timestamp > store.latest :
        pullnewest(store)

    return store.bracket(timestamp)

def recordsbetween( tbl, begin, end ):
    store = Persistence.Store("SolarDB", tbl)
    store.refreshtimebracket()

    if end > store.latest or begin > store.latest:
        pullnewest(store)

    return store.recordsbetween( begin, end )

def pullnewest(storage):
    global data
    storage.refreshtimebracket()

    with urllib.request.urlopen(storage.URL) as url:
        data = json.load(url)

    storage.begintrans()

    for row in data[1:] :
        if row[0] > storage.latest :
            storage.addrecord(row)

    storage.endtrans()

