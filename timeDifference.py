import datetime
import time

string = "2019-04-24T13:06:00"

currenttime = datetime.datetime.fromtimestamp(time.time())
datatime = time.mktime(datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S").timetuple())

datatime = datetime.datetime.fromtimestamp(datatime)

difference = currenttime - datatime

if int(str(difference)[0]) > 0:
    print("TOO OLD")

else:
    print("NEW DATA")
