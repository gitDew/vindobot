import json
import requests

class WorkitoutFetcher:
    TO_KEYS = {
            "StammNr": "StammNr",
            "PreName": "FirstName",
            "Name": "LastName",
            "Zimmernummer": "RoomNr",
            "BlockedTill": "BlockedTill"
            }

    def __init__(self):
        with open("mycreds.json") as mycredsfile:
            self.creds = json.load(mycredsfile)

    def fetch(self):
        r = requests.get(self.creds["url"])


        return [{v: e[k] for k, v in self.TO_KEYS.items()} for e in r.json()]
