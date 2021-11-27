from selenium import webdriver
# from chromedriver_py import binary_path
# driver = webdriver.Chrome(executable_path=binary_path)

class WorkitoutAuthenticator:
    def __init__(self, url, username, password, driver):
        self.url = url
        self.username = username
        self.password = password
        self.driver = driver

    def login_for_cookies(self):

        self.driver.get(self.url)
        username = self.driver.find_element_by_id("inputEmail")
        password = self.driver.find_element_by_id("inputPassword")

        username.send_keys(self.creds[self.username])
        password.send_keys(self.creds[self.password])

        form = self.driver.find_element_by_tag_name('form')
        form.submit()

        cookies = {
                "PHPSESSID": self.driver.get_cookie("PHPSESSID")["value"]
                }
        
        # cookie might expire really soon after this?
        self.driver.quit()

        return cookies
