import urllib.request, json
import os
import datetime
import time
from pushover import init, Client

lastKpParse = datetime.datetime.strptime("01011970", "%d%m%Y").date()
lastKpVal = 0
deltaTime = -1

settings = None
with open('./settings.json', 'r') as settingsF:
    settings = json.load(settingsF)

client = Client(settings['user_key'], api_token=settings['api_token'])

# Alert messages
alertMsg = "Kp index raised to: "
downgradeMsg = "Kp index back to: "
minSeverityReportLevel = 7

def parseJson():
    global lastKpParse, lastKpVal
    with urllib.request.urlopen("http://services.swpc.noaa.gov/products/noaa-planetary-k-index.json") as url:
        data = json.loads(url.read().decode())

        # find newest entry
        curdate = datetime.datetime.strptime(data[len(data)-1][0], "%Y-%m-%d %H:%M:%S.%f").date()
        if curdate > lastKpParse:
            kpVal = int(data[len(data)-1][1])
            print("New entry found at "+data[len(data)-1][0]+" with KpVal "+str(kpVal))
            if kpVal != lastKpVal:
                if lastKpVal >= minSeverityReportLevel and kpVal < lastKpVal:
                    lastKpParse = curdate
                    lastKpVal = kpVal
                    issueDowngrade(kpVal)
                elif kpVal >= minSeverityReportLevel:
                    lastKpParse = curdate
                    lastKpVal = kpVal
                    issueAlert(kpVal)

def issueAlert(val):
    text = ""
    text = alertMsg+str(val)+"\n"
    if val == 7:
        text += "Cat G3: Strong"
    elif val == 8:
        text += "Cat G4: Severe"
    elif val == 9:
        text += "Cat G5: EXTREME"
    client.send_message(text, title="SOLAR ALERT", priority=1, url="http://services.swpc.noaa.gov/images/wing-kp-24-hour.gif")

def issueDowngrade(val):
    text = downgradeMsg+str(val)
    client.send_message(text, title="Solar Downgrade", priority=1, url="http://services.swpc.noaa.gov/images/wing-kp-24-hour.gif")

if __name__ == '__main__':
    # run hourly checks
    while True:
        now = datetime.datetime.now().hour
        if deltaTime != now:
            parseJson()

        deltaTime = now

        # sleep for 10 minutes
        time.sleep(600)
