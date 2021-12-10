import pytest
from googleapiclient.discovery import build
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
