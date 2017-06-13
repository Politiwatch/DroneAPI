import csv
from strike_generator import generate_strike
from dateutil import parser
import json

def process(buffer):
    reader = csv.reader(buffer)
    first = True
    strikes = []
    for row in reader:
        if first:
            first = False
            continue
        date = parser.parse(row[1], dayfirst=True)
        supplemental = {}
        supplemental['minCiviliansKilled'] = int(row[6])
        supplemental['maxCiviliansKilled'] = int(row[7])
        supplemental['minChildrenKilled'] = int(row[8])
        supplemental['maxChildrenKilled'] = int(row[9])
        supplemental['minInjured'] = int(row[10])
        supplemental['maxInjured'] = int(row[11])
        stats = None
        references = ["TBIJ spreadsheet"]
        location = row[2].strip() + ", Pakistan"
        strike = generate_strike(row[0], date.strftime('%d %B %Y').strip(), int(row[4]), int(row[5]), stats, references, None, location, "US drone strike", supplemental)
        strikes.append(strike)
    return strikes
