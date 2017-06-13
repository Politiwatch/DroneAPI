from bs4 import BeautifulSoup
import urllib2
import json
from dateutil import parser
import re
from strike_generator import generate_strike

def parse_strike_page(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    r = opener.open(url).read()
    soup = BeautifulSoup(r, "lxml")
    strikeshtml = soup.find_all(class_="tb-c-drone-data-strike")
    strikes = []
    for strikehtml in strikeshtml:
        index = strikehtml.find(class_="tb-c-drone-data-strike__heading").get_text().split("\n")[0]
        link = strikehtml.find(class_="tb-c-drone-data-strike__link").get("href")
        if link.startswith("#"):
            link = url + link
        date = parser.parse(strikehtml.find(class_="tb-c-drone-data-strike__date").get_text())
        body = strikehtml.find_all(class_="tb-o-story-section__body")[1].get_text()
        minkilled = "-1"
        maxkilled = "-1"
        stats = []
        for stat in strikehtml.find_all(class_="tb-c-stats-list"):
            for item1 in stat.get_text().strip().split("\n"):
                for item in item1.strip().split(","):
                    stats.append(item)
                    item = item.strip()
                    if "reported killed" in item and (not "children" in item) and (not "civilians" in item):
                        if "unknown" in item.lower():
                            break
                        killed = re.search(r"([0-9]{1,}-[0-9]{1,})|([0-9]{1,})", item).group(0)
                        if "-" in killed:
                            minkilled = killed.split("-")[0]
                            maxkilled = killed.split("-")[1]
                        else:
                            minkilled = killed
                            maxkilled = killed
        typeofstrike = "unknown"
        location = "unknown"
        references = []
        for line in strikehtml.find(class_="tb-o-story-section__body").get_text().split("\n"):
            if line.lower().strip().startswith("type of strike"):
                typeofstrike = line[14:]
            if line.lower().strip().startswith("location"):
                location = line[8:]
        if typeofstrike == "?" and location == "?":
            for li in strikehtml.find_all("li"):
                line = li.get_text()
                if line.lower().strip().startswith("type of strike"):
                    typeofstrike = line[16:]
                if line.lower().strip().startswith("location"):
                    location = line[10:]
        for a in strikehtml.find_all("a"):
            href = a.get("href")
            if href.startswith("#") is not True:
                references.append(href)
        try:
            if body.index("Type of strike:") is not -1:
                body = body[:body.index("Type of strike:")]
        except ValueError:
            try:
                if body.index("Location:") is not -1:
                    body = body[:body.index("Location")]
            except ValueError:
                try:
                    if body.index("Reference:") is not -1:
                        body = body[:body.index("Reference:")]
                    if body.index("References:") is not -1:
                        body = body[:body.index("References:")]
                except ValueError:
                    pass
        strike = generate_strike(index.strip(), date.strftime('%d %B %Y').strip(), minkilled.strip(), maxkilled.strip(), [stat.strip() for stat in stats], [reference.strip() for reference in references], body.strip(), location.strip(), typeofstrike.strip(), None)
        strikes.append(strike)
    return strikes


#parse_strike_page("https://www.thebureauinvestigates.com/drone-war/data/somalia-reported-us-covert-actions-2017")
# WORKS: parse_strike_page("https://www.thebureauinvestigates.com/drone-war/data/pakistan-covert-us-reported-actions-2017")
# WORKS: parse_strike_page("https://www.thebureauinvestigates.com/drone-war/data/get-the-data-a-list-of-us-air-and-drone-strikes-afghanistan-2017")
# WORKS: parse_strike_page("https://www.thebureauinvestigates.com/drone-war/data/somalia-reported-us-covert-actions-2017")
# DOESNT WORK: parse_strike_page("https://www.thebureauinvestigates.com/drone-war/data/somalia-reported-us-covert-actions-2001-2017")
# DOESNT WORK: parse_strike_page("https://www.thebureauinvestigates.com/drone-war/data/yemen-reported-us-covert-actions-2016")
#parse_strike_page("https://www.thebureauinvestigates.com/drone-war/data/somalia-reported-us-covert-actions-2001-2017")
