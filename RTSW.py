import urllib.request, json
import Persistence
from bottle import route, run, request, response

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

@route('/cached/<tbl_name>/<command>')

def get_cached_records(tbl_name, command):

    params = {key: val for (key, val) in request.params.items()}

    response.content_type = 'application/json'

    check = Persistence.Store("SolarDB", tbl_name)

    if not check.tableexists():
        return json.dumps([{"error": "unrecognized source"}])

    if command == "between":
        return json.dumps(recordsbetween( tbl_name, params["start"], params["end"] ))
    if command == "bracket":
        return json.dumps(bracket( tbl_name, params["datetime"]))
    else:
        return json.dumps([{"error": "unrecognized command"}])

@route('/admin/addsource')

def add_new_source():
    params = {key: val for (key, val) in request.params.items()}
    response.content_type = 'application/json'

    urlstr = params["URL"]

    store = Persistence.Store("SolarDB", urlstr)

    with urllib.request.urlopen(urlstr) as url:
        data = json.load(url)

    store.addtable(urlstr, data)

    if store.tableexists():
        return json.dumps([{"success" : "cache created", "sourceshortname" : store.table}])
    else:
        return json.dumps([{"error" : "could not create a cache"}])

run(host="0.0.0.0", port=8081, reloader=True)
