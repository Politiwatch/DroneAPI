import strike_parser
import af_processor
import ym_processor
import pk_processor
import sm_processor
import json
import requests
from dateutil import parser
from StringIO import StringIO
import os

tbij_sources = [
    "https://www.thebureauinvestigates.com/drone-war/data/get-the-data-a-list-of-us-air-and-drone-strikes-afghanistan-2017",
    "https://www.thebureauinvestigates.com/drone-war/data/pakistan-covert-us-reported-actions-2017",
    "https://www.thebureauinvestigates.com/drone-war/data/somalia-reported-us-covert-actions-2017",
    "https://www.thebureauinvestigates.com/drone-war/data/yemen-reported-us-covert-actions-2017"
]

af_key = "1Q1eBZ275Znlpn05PnPO7Q1BkI3yJZbvB3JycywAmqWc"
af_id = "0"
ym_key = "1lb1hEYJ_omI8lSe33izwS2a2lbiygs0hTp2Al_Kz5KQ"
ym_id = "492674230"
sm_key = "1-LT5TVBMy1Rj2WH30xQG9nqr8-RXFVvzJE_47NlpeSY"
sm_id = "859698683"
pk_key = "1NAfjFonM-Tn7fziqiv33HlGt09wgLZDSCP-BQaux51w"
pk_id = "1436874561"

def gsheet_buffer(key, id):
    r = requests.get("https://docs.google.com/spreadsheet/ccc?key=" + key + "&gid=" + id + "&output=csv")
    # I know that a params object could be used but I choose not to use it because I don't trust the google docs URL scheme as being HTTP compliant
    return StringIO(r.text)

strikes = {}
summary = []
latest_strike = {}

totals = {
    "minKilled": 0,
    "maxKilled": 0,
    "minCiviliansKilled": 0,
    "maxCiviliansKilled": 0,
    "minChildrenKilled": 0,
    "maxChildrenKilled": 0,
    "minInjured": 0,
    "maxInjured": 0,
    "totalDroneStrikes": 0
}

def indexify(l): # indexify a list of strikes
    indexed = {}
    for element in l:
        if element is not None:
            indexed[element['index'].upper()] = element
    return indexed

def load_data():
    global strikes, totals, summary, latest_strike
    loaded_strikes = []
    loaded_strikes_indices = []
    for source in tbij_sources:
        loaded_strikes.extend(strike_parser.parse_strike_page(source))
    loaded_strikes_indices.extend([strike['index'] for strike in loaded_strikes])
    loaded_strikes = indexify(loaded_strikes)
    for strike in af_processor.process(gsheet_buffer(af_key, af_id)):
        if strike['index'].upper() in loaded_strikes_indices:
            strike['body'] = loaded_strikes[strike['index'].upper()]['body']
            strike['stats'] = loaded_strikes[strike['index'].upper()]['stats']
            strike['references'].extend(loaded_strikes[strike['index'].upper()]['references'])
        strikes[strike['index'].upper()] = strike
    for strike in ym_processor.process(gsheet_buffer(ym_key, ym_id)):
        if strike['index'].upper() in loaded_strikes_indices:
            strike['body'] = loaded_strikes[strike['index'].upper()]['body']
            strike['stats'] = loaded_strikes[strike['index'].upper()]['stats']
            strike['references'].extend(loaded_strikes[strike['index'].upper()]['references'])
        strikes[strike['index'].upper()] = strike
    for strike in sm_processor.process(gsheet_buffer(sm_key, sm_id)):
        if strike['index'].upper() in loaded_strikes_indices:
            strike['body'] = loaded_strikes[strike['index'].upper()]['body']
            strike['stats'] = loaded_strikes[strike['index'].upper()]['stats']
            strike['references'].extend(loaded_strikes[strike['index'].upper()]['references'])
        strikes[strike['index'].upper()] = strike
    for strike in pk_processor.process(gsheet_buffer(pk_key, pk_id)):
        if strike['index'].upper() in loaded_strikes_indices:
            strike['body'] = loaded_strikes[strike['index'].upper()]['body']
            strike['stats'] = loaded_strikes[strike['index'].upper()]['stats']
            strike['references'].extend(loaded_strikes[strike['index'].upper()]['references'])
        strikes[strike['index'].upper()] = strike
    # normalize locations
    for strikekey in strikes:
        strike = strikes[strikekey]
        strike['location'] = ", ".join([field.strip() for field in strike['location'].split(",") if field.strip() != '-' and field.strip().lower() != "unknown"])
    for strike in strikes.values():
        totals['minKilled'] += strike['minKilled']
        totals['maxKilled'] += strike['maxKilled']
        if 'minCiviliansKilled' in strike['supplemental']:
            totals['minCiviliansKilled'] += strike['supplemental']['minCiviliansKilled']
        if 'maxCiviliansKilled' in strike['supplemental']:
            totals['maxCiviliansKilled'] += strike['supplemental']['maxCiviliansKilled']
        if 'minChildrenKilled' in strike['supplemental']:
            totals['minChildrenKilled'] += strike['supplemental']['minChildrenKilled']
        if 'maxChildrenKilled' in strike['supplemental']:
            totals['maxChildrenKilled'] += strike['supplemental']['maxChildrenKilled']
        if 'minInjured' in strike['supplemental']:
            totals['minInjured'] += strike['supplemental']['minInjured']
        if 'maxInjured' in strike['supplemental']:
            totals['maxInjured'] += strike['supplemental']['maxInjured']
        if 'minStrikes' in strike['supplemental']:
            totals["totalDroneStrikes"] += strike['supplemental']['minStrikes']
        else:
            totals['totalDroneStrikes'] += 1
    summary = sorted(strikes.iterkeys(), key=lambda k: parser.parse(strikes[k]['date']), reverse=True)
    latest_strike = strikes[summary[0]]
    print latest_strike


def restore_data(filepath):
    global strikes, summary, latest_strike, totals
    if not os.path.exists(filepath):
        raise EnvironmentError("No backup file at '" + filepath + "' to load from!")
    with open(filepath, "r") as infile:
        data = json.load(infile)
        strikes = data['strikes']
        summary = data['summary']
        latest_strike = data['latest_strike']
        totals = data['totals']
        return data['updated']

def write_data(filepath, updated):
    outdata = {
        "strikes": strikes,
        "summary": summary,
        "latest_strike": latest_strike,
        "totals": totals,
        "updated": updated
    }
    with open(filepath, "w") as outfile:
        json.dump(outdata, outfile, sort_keys=True, indent=4)
