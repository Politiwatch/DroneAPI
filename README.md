# DroneAPI
An automatic restful API for the Bureau of Investigative Journalism's "Drone War" data. **This tool only processes DRONE STRIKES, not all covert U.S. actions.**

## How to Use
Using the DroneAPI is simple. All you need to do is navigate your code to a valid instance (I personally recommend the Politiwatch-maintained instance at https://tbij.dronescout.org) and you'll be set! The root endpoint should provide you all the information you need to get started. If that's not enough, please refer to the endpoint documentation below.

### Getting Totals
Often, all you want are totals and general statistics. To get these figures, simply navigate to `/totals`. You'll get back data which looks like the following:

```
{
    "maxChildrenKilled": 261,
    "maxCiviliansKilled": 1299,
    "maxInjured": 2349,
    "maxKilled": 8424,
    "minChildrenKilled": 202,
    "minCiviliansKilled": 613,
    "minInjured": 1557,
    "minKilled": 5819,
    "totalDroneStrikes": 1092,
    "updated": "2017-06-13 04:26:33"
}
```

### Getting a List of Strikes
To get a list of all the strikes, navigate to `/summary`. You'll get an unabridged version of the following data back:

```
{
    "strikes": [
        "YEM139",
        "YEM138",
        "AFG208",
        ...
        "AFG345",
        "AFG347",
        "AFG346",
        "AFG252"
    ],
    "totals": {
        "maxChildrenKilled": 261,
        "maxCiviliansKilled": 1299,
        "maxInjured": 2349,
        "maxKilled": 8424,
        "minChildrenKilled": 202,
        "minCiviliansKilled": 613,
        "minInjured": 1557,
        "minKilled": 5819,
        "totalDroneStrikes": 1092
    },
    "updated": "2017-06-13 04:26:33"
}
```

### Getting Data on a Particular Strike
To get the detailed data on a particular strike, navigate to `/strike` and include the strike ID as the parameter `strike`. An example relative request URL could look like the following: `/strike?strike=AFG346`. This should give the following response:

```
{
    "body": "Four members of Afghanistan's branch of Islamic State, including a commander of the group, were killed in a US strike in Nangarhar province, Attaullah Khogyani, the governor\u2019s spokesman, told Pajhwok. \u00a0\nA statement from the \"provincial police commandment\" reported in Khaama press said a drone strike killed three members of the group, including a local leader, identified as Asadullah.\u00a0\nThe date of the strike was not clear, but both media sites reported it on May 29.",
    "date": "29 May 2017",
    "index": "AFG346",
    "location": "Spina Zhai, Nazian, Nangarhar, Afghanistan",
    "maxKilled": 4,
    "minKilled": 3,
    "references": [
        "TBIJ spreadsheet",
        "http://www.khaama.com/us-drone-strike-kills-isis-leader-and-his-2-fighters-in-east-of-afghanistan-02814",
        "http://www.pajhwok.com/en/2017/05/29/4-daesh-rebels-including-commander-killed-nangarhar"
    ],
    "stats": [
        "3-4 reported killed"
    ],
    "supplemental": {
        "maxChildrenKilled": 0,
        "maxCiviliansKilled": 0,
        "maxInjured": 0,
        "maxStrikes": 1,
        "minChildrenKilled": 0,
        "minCiviliansKilled": 0,
        "minInjured": 0,
        "minStrikes": 1,
        "usaConfirmed": false,
        "usaIsOnlySource": false
    },
    "type": "US strike",
    "updated": "2017-06-13 04:23:51"
}
```
*Note that only strikes which took place after 1 Jan 2017 will have a non-null body.*

## How to Deploy Yourself
Run `api.py` with the working directory set to wherever you'd like the backup data (`strikes.json`) to be saved to. The server will start on port `8888` automatically.
