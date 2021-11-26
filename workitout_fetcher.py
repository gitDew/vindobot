import requests
from credentials import MyCredentials
from selenium import webdriver
from chromedriver_py import binary_path

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
        
    def login_to_get_cookies(self):
        driver = webdriver.Chrome(executable_path=binary_path)

        driver.get(self.creds["url"])
        username = driver.find_element_by_id("inputEmail")
        password = driver.find_element_by_id("inputPassword")

        username.send_keys(self.creds["username"])
        password.send_keys(self.creds["password"])

        form = driver.find_element_by_tag_name('form')
        form.submit()

        cookies = {
                "PHPSESSID": driver.get_cookie("PHPSESSID")["value"]
                }

        driver.quit()

        return cookies

    def fetch(self, cookies):
        r = requests.get(self.creds["data_url"], cookies=cookies)
        return [{v: e[k] for k, v in self.TO_KEYS.items()} for e in r.json()]

