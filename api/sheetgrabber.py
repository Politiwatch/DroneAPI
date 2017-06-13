import gspread

def grab(sheet_url):
    client = gspread.Client(None)
    wkb = client.open_by_url(sheet_url)
    print wkb
