import json

class MyCredentials:
    def __init__(self):
        self.credentials = None

    def _load_from_file(self):
        with open("mycreds.json") as credsfile:
            return json.load(credsfile)
    
    def get_credentials(self):
        if not self.credentials:
            self.credentials = self._load_from_file()
        return self.credentials
