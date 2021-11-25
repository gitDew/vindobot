import json

class MyCredentials:
    creds = None
    def load_from_file():
        with open("mycreds.json") as credsfile:
            MyCredentials.creds = json.load(credsfile)
        return MyCredentials.creds
