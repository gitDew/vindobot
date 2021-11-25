import requests
from credentials import MyCredentials

class WorkitoutFetcher:
    TO_KEYS = {
            "StammNr": "StammNr",
            "PreName": "FirstName",
            "Name": "LastName",
            "Zimmernummer": "RoomNr",
            "BlockedTill": "BlockedTill"
            }

    def __init__(self):
        self.creds = MyCredentials.load_from_file()

    def fetch(self):
        r = requests.get(self.creds["url"])


        return [{v: e[k] for k, v in self.TO_KEYS.items()} for e in r.json()]
