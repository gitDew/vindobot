import pytest
import responses
import requests

from workitout_fetcher import WorkitoutFetcher
from credentials import MyCredentials

class TestWorkitoutFetcher:
    @pytest.fixture
    def valid_workitout_fetcher(self):
        cookies = {"PHPSESSID": "abcdefghi"}
        return WorkitoutFetcher("https://www.workitoutserver.com/api/students", cookies)

    @responses.activate
    def test_successful_fetch(self, valid_workitout_fetcher):
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
        responses.add(responses.GET, "https://www.workitoutserver.com/api/students",
                json=[student1, student2]) 
        
        students = valid_workitout_fetcher.fetch()

        assert students[0] == {"StammNr": "123456", "FirstName": "John", "LastName": "Doe", "RoomNr": "999", "BlockedTill": "2021-12-31 00:00:00"}
        assert students[1] == {"StammNr": "123460", "FirstName": "Jane", "LastName": "Marrone", "RoomNr": "120", "BlockedTill": "0000-00-00 00:00:00"}
        assert {"StammNr", "FirstName", "LastName", "RoomNr", "BlockedTill"} == set(students[0].keys())
        
