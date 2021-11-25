import pytest
import responses
import requests

from workitout_fetcher import WorkitoutFetcher
from credentials import MyCredentials

class TestWorkitoutFetcher:

    @pytest.fixture
    def creds(self):
        return MyCredentials.load_from_file()

    @pytest.fixture
    def workitout_fetcher(self):
        return WorkitoutFetcher()

    def test_it_compiles(self, workitout_fetcher):
        assert True

    @responses.activate
    def test_status_code_200(self, workitout_fetcher, creds):
        responses.add(responses.GET, creds["url"], status=200)

        resp = requests.get(creds["url"]) 

        assert resp.status_code == 200

    @responses.activate
    def test_given_timeout_then_exception_is_raised(self, workitout_fetcher, creds):
        responses.add(responses.GET, creds["url"], body=requests.Timeout())

        with pytest.raises(requests.Timeout):
            workitout_fetcher.fetch()

    @responses.activate
    def test_successful_fetch(self, workitout_fetcher, creds):

        student1 = {
                "ID": "688",
                "PreName": "John",
                "Name": "Doe",
                "StammNr": "123456",
                "Zimmernummer": "999",
                "IDHaus": "...",
                "Tel": "...",
                "Mail": "...",
                "BlockedTill": "2021-12-31 00:00:00",
                "Active": "...",
                "Logging": "0",
                "MAC": [
                    "..."
                    ],
                "IP": [
                    "..."
                    ],
                "Status": "...",
                "HausName": "...",
                "HausNameShort": "..."
                }
        student2 = {
                "ID": "689",
                "PreName": "Jane",
                "Name": "Marrone",
                "StammNr": "123460",
                "Zimmernummer": "120",
                "IDHaus": "...",
                "Tel": "...",
                "Mail": "...",
                "BlockedTill": "0000-00-00 00:00:00",
                "Active": "...",
                "Logging": "0",
                "MAC": [
                    "..."
                    ],
                "IP": [
                    "..."
                    ],
                "Status": "...",
                "HausName": "...",
                "HausNameShort": "..."
                }
        responses.add(responses.GET, creds["url"],
                json=[student1, student2]) 

        students = workitout_fetcher.fetch()

        assert students[1] == {"StammNr": "123460", "FirstName": "Jane", "LastName": "Marrone", "RoomNr": "120", "BlockedTill": "0000-00-00 00:00:00"}
        assert {"StammNr", "FirstName", "LastName", "RoomNr", "BlockedTill"} == set(students[0].keys())
        
