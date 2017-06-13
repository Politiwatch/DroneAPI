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
        if "drone" in row[5] or int(row[4]) is 1:
            date = parser.parse(row[1], dayfirst=True)
            supplemental = {}
            supplemental['usaConfirmed'] = row[3] is "Confirmed"
            supplemental['minStrikes'] = int(row[6])
            supplemental['maxStrikes'] = int(row[7])
            supplemental['minCiviliansKilled'] = int(row[10])
            supplemental['maxCiviliansKilled'] = int(row[11])
            supplemental['minChildrenKilled'] = int(row[12])
            supplemental['maxChildrenKilled'] = int(row[13])
            supplemental['minInjured'] = int(row[14])
            supplemental['maxInjured'] = int(row[15])
            stats = None
            references = ["TBIJ spreadsheet"]
            location = row[2].strip() + ", Somalia"
            strike = generate_strike(row[0], date.strftime('%d %B %Y').strip(), int(row[8]), int(row[9]), stats, references, None, location, row[5], supplemental)
            strikes.append(strike)
    return strikes
