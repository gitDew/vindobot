import requests

class WorkitoutFetcher:
    TO_KEYS = {
            "StammNr": "StammNr",
            "PreName": "FirstName",
            "Name": "LastName",
            "Zimmernummer": "RoomNr",
            "BlockedTill": "BlockedTill"
            }

    def __init__(self, url, cookies):
        self.url = url
        self.cookies = cookies

    def fetch(self):
        r = requests.get(self.url, cookies=self.cookies)
        return [{v: e[k] for k, v in self.TO_KEYS.items()} for e in r.json()]

