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
        if "drone" in row[4] or int(row[6]) is 1:
            date = parser.parse(row[1], dayfirst=True)
            supplemental = {}
            supplemental['usaConfirmed'] = row[5] is "Confirmed"
            supplemental['minStrikes'] = int(row[7])
            supplemental['maxStrikes'] = int(row[8])
            supplemental['minCiviliansKilled'] = int(row[11])
            supplemental['maxCiviliansKilled'] = int(row[12])
            supplemental['minChildrenKilled'] = int(row[13])
            supplemental['maxChildrenKilled'] = int(row[14])
            supplemental['minInjured'] = int(row[15])
            supplemental['maxInjured'] = int(row[16])
            stats = None
            references = ["TBIJ spreadsheet"]
            location = row[2].strip() + ", " + row[3].strip() + ", Yemen"
            strike = generate_strike(row[0], date.strftime('%d %B %Y').strip(), int(row[9]), int(row[10]), stats, references, None, location, row[4], supplemental)
            strikes.append(strike)
    return strikes
