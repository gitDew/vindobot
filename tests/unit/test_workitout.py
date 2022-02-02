import pytest
import responses
import requests
import workitout

class TestWorkitoutFetcher:
    @pytest.fixture
    def logged_in_workitout(self):
        cookies = {"PHPSESSID": "abcdefg"}
        return workitout.Fetcher("https://www.workitoutserver.com/api/students", cookies)

    @responses.activate
    def test_successful_fetch(self, logged_in_workitout):
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
        
        students = logged_in_workitout.fetch()

        assert students[0] == {"StammNr": "123456", "FirstName": "John", "LastName": "Doe", "RoomNr": "999", "BlockedTill": "31.12.2021"}
        assert students[1] == {"StammNr": "123460", "FirstName": "Jane", "LastName": "Marrone", "RoomNr": "120", "BlockedTill": ""}
        assert {"StammNr", "FirstName", "LastName", "RoomNr", "BlockedTill"} == set(students[0].keys())
        
