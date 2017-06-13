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
        if int(row[6]) is 1:
            date = parser.parse(row[1], dayfirst=True)
            supplemental = {}
            supplemental['usaConfirmed'] = int(row[7]) is 1
            supplemental['usaIsOnlySource'] = int(row[8]) is 1
            if row[11] is not '-':
                supplemental['time'] = row[11].strip()
            supplemental['minStrikes'] = int(row[13])
            supplemental['maxStrikes'] = int(row[14])
            supplemental['minCiviliansKilled'] = int(row[17])
            supplemental['maxCiviliansKilled'] = int(row[18])
            supplemental['minChildrenKilled'] = int(row[19])
            supplemental['maxChildrenKilled'] = int(row[20])
            supplemental['minInjured'] = int(row[21])
            supplemental['maxInjured'] = int(row[22])
            stats = None
            references = ["TBIJ spreadsheet"]
            location = row[2].strip() + ", " + row[3].strip() + ", " + row[4].strip() + ", Afghanistan"
            strike = generate_strike(row[0], date.strftime('%d %B %Y').strip(), int(row[15]), int(row[16]), stats, references, None, location, row[5], supplemental)
            strikes.append(strike)
    return strikes
