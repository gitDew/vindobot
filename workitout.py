import requests
from selenium import webdriver
# from chromedriver_py import binary_path
# driver = webdriver.Chrome(executable_path=binary_path)

class Fetcher:
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
        fetched = [{v: e[k] for k, v in self.TO_KEYS.items()} for e in r.json()]
        return self._clean_blocked_date(fetched)

    def _clean_blocked_date(self, fetched):
        for student in fetched:
            if student["BlockedTill"] == "0000-00-00 00:00:00":
                student["BlockedTill"] = ""
            else:
                y, m, d = student["BlockedTill"].split()[0].split('-')
                student["BlockedTill"] = f"{d}.{m}.{y}"
        return fetched

class Authenticator:
    def __init__(self, url, selenium_driver):
        self.url = url
        self.driver = selenium_driver

    def login_for_cookies(self, username, password):

        self.driver.get(self.url)
        username_element = self.driver.find_element_by_id("inputEmail")
        password_element = self.driver.find_element_by_id("inputPassword")

        username_element.send_keys(username)
        password_element.send_keys(password)

        form_element = self.driver.find_element_by_tag_name('form')
        form_element.submit()

        cookies = {
                "PHPSESSID": self.driver.get_cookie("PHPSESSID")["value"]
                }
        
        # TODO cookie might expire really soon after this?
        self.driver.quit()

        return cookies
