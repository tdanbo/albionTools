import json
import os

# - dataset - #
catagories = ["melee","mounts","ranged"]
tiers = ["1","2","3","4","5","6","7","8"]

for category in catagories:
    for tier in tiers:
        path = "/lucas/ilm/dept/dms/sand/tdanbo/wipscripts/apiTest/%s_%s" % (category,tier)
        if os.path.isfile(path):
            file = open(path, "r")
            datastore = json.load(file)
            with open(path) as json_file:  
                data = json.load(json_file)
                for i in data:
                    print i["item_id"]
                    print i["city"]
                    print ""
        else:
            pass
