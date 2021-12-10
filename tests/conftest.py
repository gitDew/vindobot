import pytest
from googleapiclient.discovery import build
from student import Student
import google_sheets

@pytest.fixture(scope="module")
def sheet_values_obj():
    creds = google_sheets.authenticate()
    service = build('sheets', 'v4', credentials=creds)
    sheet_values_obj = service.spreadsheets().values()
    return sheet_values_obj

@pytest.fixture(scope="module")
def request_factory(sheet_values_obj):
    spreadsheet_ID = "1Du82nqXiMQR1aQ5k_vzTvCkgDYthT8-e9HGi-_JfY_c" 
    return google_sheets.RequestFactory(sheet_values_obj, spreadsheet_ID)

@pytest.fixture(scope="module")
def reader(request_factory):
    return google_sheets.Reader(request_factory)

@pytest.fixture(scope="module")
def writer(request_factory):
    return google_sheets.Writer(request_factory)

@pytest.fixture
def paying_example_student():
    student_entry = {"RowID": 9, "StammNr": "123456", "FirstName": "Martin", "LastName": "Scorsese", 
            "RoomNr": "987", "BlockedTill": "", "From": "01.01.2021", "To": "01.04.2021", "Comment": "Shutter Island was great"}
    return Student(student_entry)

@pytest.fixture
def blocked_example_student():
    student_entry = {"RowID": 10, "StammNr": "123457", "FirstName": "Bad", "LastName": "Man", 
            "RoomNr": "666", "BlockedTill": "01.12.2021", "From": "01.01.2021", "To": "01.02.2021", "Comment": ""}
    return Student(student_entry)

@pytest.fixture
def expired_but_not_blocked_example_student():
    student_entry = {"RowID": 11, "StammNr": "123458", "FirstName": "Sneaky", "LastName": "Man", 
            "RoomNr": "667", "BlockedTill": "", "From": "01.01.2021", "To": "05.02.2021", "Comment": "Careful, this guy is sneaky"}
    return Student(student_entry)

@pytest.fixture
def uncertain_example_student():
    student_entry = {"RowID": 12, "StammNr": "123459", "FirstName": "Johnny", "LastName": "Uncertain", 
            "RoomNr": "", "BlockedTill": "", "From": "", "To": "", "Comment": "?"}
    return Student(student_entry)

@pytest.fixture
def uncertain_blocked_example_student():
    student_entry = {"RowID": 12, "StammNr": "123459", "FirstName": "Johnny", "LastName": "Uncertain", 
            "RoomNr": "", "BlockedTill": "01.12.2021", "From": "", "To": "", "Comment": "?"}
    return Student(student_entry)
