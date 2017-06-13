import tornado.ioloop
import tornado.web
import json
import strike_manager
from time import gmtime, strftime

starttime = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

def error(response, code, message):
    response.clear()
    response.set_status(code)
    response.set_header("Content-Type", "application/json")
    data = {
        "response": "error",
        "code": code,
        "issue": message
    }
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
        self.render("gui/index.html", totals=strike_manager.totals, summary=strike_manager.summary)
        self.write(unicode(json.dumps(data, sort_keys=True, indent=4)))
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
                    "endpoint": "/totals",
                    "parameters": [],
                    "description": "get the various totals (i.e. total killed, total civilians killed, etc)",
                    "exampleUrl": "https://tbij.dronescout.org/totals"
                },
                {
                    "endpoint": "/",
                    "parameters": [],
                    "description": "index",
                    "exampleUrl": "https://tbij.dronescout.org/"
                },
            ],
            "updated": starttime
        }
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.write(unicode(json.dumps(out, sort_keys=True, indent=4)))
print "Loading data..."
strike_manager.load_data()
print strike_manager.totals
print "Backing up data..."
strike_manager.write_data("strikes.json")
print "Assembling API..."
application = tornado.web.Application([
    (r"/api", IndexHandler),
    (r"/", GuiHandler),
    (r"/summary", SummaryHandler),
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
