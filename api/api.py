import tornado.ioloop
import tornado.web
import json
import strike_manager
from time import gmtime, strftime
import sys
from datetime import date
import dateutil
import csv

starttime = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

source = "TBIJ"
source_long = "The Bureau of Investigative Journalism"
source_url = "https://www.thebureauinvestigates.com/projects/drone-war"

def error(response, code, message):
    response.clear()
    response.set_status(code)
    response.set_header("Content-Type", "application/json")
    data = {
        "response": "error",
        "code": code,
        "issue": message
    }
    response.set_header("Access-Control-Allow-Origin", "*")
    response.finish(json.dumps(data, indent=4, sort_keys=True))
class StrikeHandler(tornado.web.RequestHandler):
    def get(self):
        if "strike" not in self.request.arguments:
            error(self, 400, "no strike given")
            return
        strike = self.get_argument("strike").upper()
        if strike not in strike_manager.strikes:
            error(self, 400, "no such strike")
            return
        data = strike_manager.strikes[strike]
        data["updated"] = starttime
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(unicode(json.dumps(data, sort_keys=True, indent=4)))
class LatestHandler(tornado.web.RequestHandler):
    def get(self):
        data = strike_manager.latest_strike
        data["updated"] = starttime
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(unicode(json.dumps(data, sort_keys=True, indent=4)))
class SummaryHandler(tornado.web.RequestHandler):
    def get(self):
        data = {
            "strikes": strike_manager.summary,
            "totals": strike_manager.totals,
            "updated": starttime
        }
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.write(unicode(json.dumps(data, sort_keys=True, indent=4)))
class DataHandler(tornado.web.RequestHandler):
    def get(self):
        data = strike_manager.strikes
        data['updated'] = starttime
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.write(unicode(json.dumps(data, sort_keys=True, indent=4)))
class GuiHandler(tornado.web.RequestHandler):
    def get(self):
        print strike_manager.latest_strike
        mm = date.today().month
        dd = date.today().day
        yyyy = date.today().year
        self.render("pages/index.html", mm=mm, dd=dd, yyyy=yyyy, source=source, source_long=source_long, source_url=source_url, totals=strike_manager.totals, summary=strike_manager.summary, updated=starttime, latest=strike_manager.latest_strike, latest_json=json.dumps(strike_manager.latest_strike, indent=4))
class TotalsHandler(tornado.web.RequestHandler):
    def get(self):
        data = strike_manager.totals
        data["updated"] = starttime
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.write(unicode(json.dumps(data, sort_keys=True, indent=4)))
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        out = {
            "creator": "Politiwatch",
            "api": "DroneAPI (RESTFUL)",
            "url": "tbij.dronescout.org",
            "license": "CC-BY",
            "notes": "This tool only includes DRONE STRIKE DATA. The tool IGNORES other covert actions. Please keep this in mind when comparing data to other aggregations.",
            "credit": "The Bureau of Investigative Journalism (https://www.thebureauinvestigates.com/projects/drone-war)",
            "source": "https://github.com/Politiwatch/DroneAPI",
            "endpoints": [
                {
                    "endpoint": "/strike",
                    "parameters": [
                        {
                            "parameter": "strike",
                            "description": "the alphanumeric strike ID assigned by the Bureau (not case sensitive)"
                        }
                    ],
                    "description": "get the data on a particular strike",
                    "exampleUrl": "https://tbij.dronescout.org/strike?strike=AFG200"
                },
                {
                    "endpoint": "/summary",
                    "parameters": [],
                    "description": "get a list of strikes",
                    "exampleUrl": "https://tbij.dronescout.org/summary"
                },
                {
                    "endpoint": "/latest",
                    "parameters": [],
                    "description": "get the latest strike",
                    "exampleUrl": "https://tbij.dronescout.org/latest"
                },
                {
                    "endpoint": "/totals",
                    "parameters": [],
                    "description": "get the various totals (i.e. total killed, total civilians killed, etc)",
                    "exampleUrl": "https://tbij.dronescout.org/totals"
                },
                {
                    "endpoint": "/api",
                    "parameters": [],
                    "description": "this index page",
                    "exampleUrl": "https://tbij.dronescout.org/"
                },
            ],
            "updated": starttime
        }
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.write(unicode(json.dumps(out, sort_keys=True, indent=4)))

def generate_csv():
    with open("pages/assets/strikes.csv", "wb") as strikecsv:
        writer = csv.writer(strikecsv, quoting=csv.QUOTE_ALL)
        writer.writerow(["INDEX", "DATE", "TYPE", "LOCATION", "MAX KILLED", "MIN KILLED", "MAX CHILDREN KILLED", "MIN CHILDREN KILLED", "MAX CIVILIANS KILLED", "MIN CIVILIANS KILLED", "MAX INJURIES", "MIN INJURIES"])
        for strike in sorted(strike_manager.strikes.values(), key=lambda k: dateutil.parser.parse(k['date'])):
            # INDEX, DATE, TYPE, LOCATION, MAX KILLED, MIN KILLED, MAX CHILDREN KILLED, MIN CHILDREN KILLED, MAX CIVILIANS KILLED, MIN CIVILIANS KILLED, MAX INJURIES, MIN INJURIES
            _index = strike['index']
            _date = strike['date']
            _type = strike['type']
            _location = strike['location']
            _maxkilled = strike['maxKilled']
            _minkilled = strike['minKilled']
            _maxchildren = ""
            if 'maxChildrenKilled' in strike['supplemental']:
                _maxchildren = strike['supplemental']['maxChildrenKilled']
            _minchildren = ""
            if 'minChildrenKilled' in strike['supplemental']:
                _minchildren = strike['supplemental']['minChildrenKilled']
            _maxcivilians = ""
            if 'maxCiviliansKilled' in strike['supplemental']:
                _maxcivilians = strike['supplemental']['maxCiviliansKilled']
            _mincivilians = ""
            if 'minCiviliansKilled' in strike['supplemental']:
                _mincivilians = strike['supplemental']['minCiviliansKilled']
            _maxinjuries = ""
            if 'maxInjured' in strike['supplemental']:
                _maxinjuries = strike['supplemental']['maxInjured']
            _mininjuries = ""
            if 'minInjured' in strike['supplemental']:
                _mininjuries = strike['supplemental']['minInjured']
            writer.writerow([_index, _date, _type, _location, _maxkilled, _minkilled, _maxchildren, _minchildren, _maxcivilians, _mincivilians, _maxinjuries, _mininjuries])
        strikecsv.close()

if "offline" in sys.argv:
    print "Loading from backup..."
    starttime = strike_manager.restore_data("strikes.json")
else:
    try:
        print "Loading data from online sources..."
        strike_manager.load_data()
        print "Backing up data..."
        strike_manager.write_data("strikes.json", starttime)
    except:
        print "Unable to load data from external sources, falling back to old data!"
        starttime = strike_manager.restore_data("strikes.json")
print strike_manager.totals
print "Assembling CSV..."
generate_csv()
print "Assembling API..."
application = tornado.web.Application([
    (r"/api", IndexHandler),
    (r"/", GuiHandler),
    (r"/summary", SummaryHandler),
    (r"/latest", LatestHandler),
    (r"/strike", StrikeHandler),
    (r"/totals", TotalsHandler),
    (r"/data", DataHandler),
    (r'/assets/(.*)$', tornado.web.StaticFileHandler, {'path': "pages/assets"})
    ])
print "Going online with data as of " + starttime
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

# tornado is a beautiful thing....
