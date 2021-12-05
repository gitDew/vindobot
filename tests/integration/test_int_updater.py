import pytest
import unittest
from csv import DictReader
from unittest.mock import MagicMock
from updater import Updater

@pytest.fixture
def example_students():
    return [{'StammNr': '1100650',
      'FirstName': 'John',
      'LastName': 'Lennon',
      'RoomNr': '305',
      'BlockedTill': ''},
     {'StammNr': '1408000',
      'FirstName': 'Bon',
      'LastName': 'Jovi',
      'RoomNr': '712',
      'BlockedTill': ''},
     {'StammNr': '1601200',
      'FirstName': 'Keith',
      'LastName': 'Richard',
      'RoomNr': '608',
      'BlockedTill': ''},
     {'StammNr': '1701000',
      'FirstName': 'Alice',
      'LastName': 'Cooper',
      'RoomNr': '704',
      'BlockedTill': ''},
     {'StammNr': '1703123',
      'FirstName': 'Axl',
      'LastName': 'Rose',
      'RoomNr': '515',
      'BlockedTill': ''}]

@pytest.fixture
def mock_fetcher(example_students):
    fetcher = MagicMock()
    fetcher.fetch.return_value = example_students
    return fetcher

@pytest.fixture
def updater(mock_fetcher, reader, writer):
    return Updater(mock_fetcher, reader, writer) 

def test_given_unchanged_diff_is_empty(updater):
    changes, new = updater.diff()

    assert changes == []
    assert new == []

def test_given_new_student_only_new_has_stuff(updater, example_students):
    example_students.append({'StammNr': '7',
      'FirstName': 'James',
      'LastName': 'Bond',
      'RoomNr': '7',
      'BlockedTill': ''})
    changes, new = updater.diff()

    assert changes == []
    assert new == [{'StammNr': '7',
      'FirstName': 'James',
      'LastName': 'Bond',
      'RoomNr': '7',
      'BlockedTill': ''}]

def test_given_existing_student_with_new_data_only_they_get_updated(updater, example_students):
    example_students[3]["LastName"] = "Wonderland"
    example_students[3]["RoomNr"] = "666"

    changes, new = updater.diff()

    assert new == []
    assert changes == [{"RowID": 5, "diff": [None, None, "Wonderland", "666", None]}]

def test_given_update_and_new_student_both_get_added(updater, example_students):
    example_students.append({'StammNr': '0000007',
      'FirstName': 'James',
      'LastName': 'Bond',
      'RoomNr': '007',
      'BlockedTill': ''})

    example_students[3]["LastName"] = "Wonderland"
    example_students[3]["RoomNr"] = "666"

    changes, new = updater.diff()

    assert new == [{'StammNr': '0000007',
      'FirstName': 'James',
      'LastName': 'Bond',
      'RoomNr': '007',
      'BlockedTill': ''}]
    assert changes == [{"RowID": 5, "diff": [None, None, "Wonderland", "666", None]}]

def test_given_multiple_changes_all_get_added(updater, example_students):
    example_students[3]["LastName"] = "Wonderland"
    example_students[3]["RoomNr"] = "666"
    example_students[0]["RoomNr"] = "123"
    example_students[4]["FirstName"] = "Jesus"

    changes, new = updater.diff()

    assert new == []
    assert changes == [
            {"RowID": 2, "diff": [None, None, None, "123", None]},
            {"RowID": 5, "diff": [None, None, "Wonderland", "666", None]},
            {"RowID": 6, "diff": [None, "Jesus", None, None, None]}
            ]

def test_given_multiple_new_all_get_added(updater, reader, writer, example_students):
    example_students.append({'StammNr': '0000007',
      'FirstName': 'James',
      'LastName': 'Bond',
      'RoomNr': '007',
      'BlockedTill': ''})
    example_students.append({'StammNr': '7777777',
      'FirstName': 'Lucky',
      'LastName': 'Man',
      'RoomNr': '777',
      'BlockedTill': '24.12.2022'})
    changes, new = updater.diff()

    assert changes == []
    assert new == [{'StammNr': '0000007',
      'FirstName': 'James',
      'LastName': 'Bond',
      'RoomNr': '007',
      'BlockedTill': ''},
      {'StammNr': '7777777',
      'FirstName': 'Lucky',
      'LastName': 'Man',
      'RoomNr': '777',
      'BlockedTill': '24.12.2022'}
      ]

    updater.add(new)
    
    values = reader.read("A197:H198")     # Test sheet has a table from 1 to 196
    writer.clear("A197:H198")

    assert values == [
            ["7", "James", "Bond", "7"],
            ["7777777", "Lucky", "Man", "777", "24.12.2022"]
            ]

def test_given_multiple_new_can_be_changed(updater, reader, writer, example_students):
    example_students.append({'StammNr': '7',
      'FirstName': 'James',
      'LastName': 'Bond',
      'RoomNr': '7',
      'BlockedTill': ''})
    example_students.append({'StammNr': '7777777',
      'FirstName': 'Lucky',
      'LastName': 'Man',
      'RoomNr': '777',
      'BlockedTill': '24.12.2022'})
    changes, new = updater.diff()

    assert len(changes) == 0
    updater.add(new)
    
    example_students[-2]["LastName"] = "Marrone"
    example_students[-1]["RoomNr"] = "888"
    example_students[-1]["BlockedTill"] = ""
    
    changes, new = updater.diff()
    assert len(changes) > 0
    assert new == []

    updater.update(changes)

    values = reader.read("A197:H198")     # Test sheet has a table from 1 to 196
    writer.clear("A197:H198")

    assert values == [
            ["7", "James", "Marrone", "7"],
            ["7777777", "Lucky", "Man", "888"]
            ]
