import pytest
from credentials import MyCredentials
from selenium import webdriver
from chromedriver_py import binary_path
import workitout

@pytest.fixture(scope="session")
def creds():
    credentials = MyCredentials()
    return credentials.get_credentials()

@pytest.fixture(scope="session")
def cookie(creds):
    driver = webdriver.Chrome(executable_path=binary_path)

    auth = workitout.Authenticator(creds["url"], driver)    

    cookie = auth.login_for_cookies(creds["username"], creds["password"])
    return cookie
    
def test_logging_in(cookie):
    assert "PHPSESSID" in cookie

def test_fetching_students(cookie, creds):
    fetcher = workitout.Fetcher(creds["data_url"], cookie)

    students = fetcher.fetch()

    assert len(students) > 0, "Fetched list should not be empty"
 
    assert {"StammNr", "FirstName", "LastName", "RoomNr", "BlockedTill"} == set(students[0].keys()), "Keys should match"
