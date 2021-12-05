import pytest
import unittest
from unittest.mock import MagicMock
from updater import Updater

def test_diff_and_new():
    students = [
            {"StammNr": "123456", "FirstName": "Cunci", "LastName": "Mokus", 
                "RoomNr": "999", "BlockedTill": "2021-12-31 00:00:00"},
            {"StammNr": "20000", "FirstName": "Janos", "LastName": "Pal", 
                "RoomNr": "777", "BlockedTill": ""},
            {"StammNr": "123460", "FirstName": "Bunci", "LastName": "Marrone", 
                "RoomNr": "666", "BlockedTill": ""}
            ]

    entries = [
            {"RowID": 100, "StammNr":"123456", "FirstName": "John", "LastName": "Serious", "RoomNr": "999", "BlockedTill": "2021-12-31 00:00:00", "From":"01.01.2022", "To":"01.02.2022", "Comment": "Serious guy"},
            {"RowID": 102, "StammNr":"123460", "FirstName": "Jane", "LastName": "Marrone", "RoomNr": "120", "BlockedTill": "", "From":"", "To":"", "Comment": ""}
            ]

    fetcher = MagicMock()
    reader = MagicMock()

    fetcher.fetch.return_value = students
    reader.getAllEntries.return_value = entries

    updater = Updater(fetcher, reader, None) 

    diff, new = updater.diff()
    assert diff == [{"RowID": 100, "diff": [None, "Cunci", "Mokus", None, None]},
                    {"RowID": 102, "diff": [None, "Bunci", None, "666", None]}]
    
    assert new == [{"StammNr": "20000", "FirstName": "Janos", "LastName": "Pal", 
                "RoomNr": "777", "BlockedTill": ""}]

def test_diff():
    students = [
            {"StammNr": "123456", "FirstName": "Cunci", "LastName": "Mokus", 
                "RoomNr": "999", "BlockedTill": "2021-12-31 00:00:00"},
            {"StammNr": "20000", "FirstName": "John", "LastName": "Paul", 
                "RoomNr": "777", "BlockedTill": ""},
            {"StammNr": "123460", "FirstName": "Bunci", "LastName": "Marrone", 
                "RoomNr": "666", "BlockedTill": ""}
            ]

    entries = [
            {"RowID": 100, "StammNr":"123456", "FirstName": "John", "LastName": "Serious", "RoomNr": "999", "BlockedTill": "2021-12-31 00:00:00", "From":"01.01.2022", "To":"01.02.2022", "Comment": "Serious guy"},
            {"RowID": 101, "StammNr":"20000", "FirstName": "Janos", "LastName": "Pal", "RoomNr": "777", "BlockedTill": "", "From":"", "To":"", "Comment": "literally the pope"},
            {"RowID": 102, "StammNr":"123460", "FirstName": "Jane", "LastName": "Marrone", "RoomNr": "120", "BlockedTill": "", "From":"", "To":"", "Comment": ""}
            ]

    fetcher = MagicMock()
    reader = MagicMock()

    fetcher.fetch.return_value = students
    reader.getAllEntries.return_value = entries

    updater = Updater(fetcher, reader, None) 

    diff, new = updater.diff()
    assert diff == [{"RowID": 100, "diff": [None, "Cunci", "Mokus", None, None]},
                    {"RowID": 101, "diff": [None, "John", "Paul", None, None]},
                    {"RowID": 102, "diff": [None, "Bunci", None, "666", None]}]
    
    assert new == []
