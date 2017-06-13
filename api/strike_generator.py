def generate_strike(index, date, minkilled, maxkilled, stats, references, body, location, typeofstrike, supplemental):
    if stats is None:
        stats = []
    if references is None:
        references = []
    return {
        "index": index.strip(),
        "date": date.strip(),
        "minKilled": int(minkilled),
        "maxKilled": int(maxkilled),
        "stats": [stat.strip() for stat in stats],
        "references": [reference.strip() for reference in references],
        "body": body,
        "location": location.strip(),
        "type": typeofstrike.strip(),
        "supplemental": supplemental
    }
