from googleapiclient.discovery import build
import google_sheets
import pytest
from credentials import MyCredentials


@pytest.fixture()
def sheet_values_obj():
    creds = google_sheets.authenticate()
    service = build('sheets', 'v4', credentials=creds)
    sheet_values_obj = service.spreadsheets().values()
    return sheet_values_obj

@pytest.fixture()
def request_factory(sheet_values_obj):
    spreadsheet_ID = "1Du82nqXiMQR1aQ5k_vzTvCkgDYthT8-e9HGi-_JfY_c" 
    return google_sheets.RequestFactory(sheet_values_obj, spreadsheet_ID)

@pytest.fixture()
def reader(request_factory):
    return google_sheets.Reader(request_factory)

@pytest.fixture()
def writer(request_factory):
    return google_sheets.Writer(request_factory)

def test_fetching(reader):
    values = reader.read("A1:AH")
    assert len(values) > 0, "Fetched list should not be empty"
    assert "StammNr" in values[0], "First row should include StammNr"

def test_writing(writer, reader):
    writer.updateRow(300, ["Hello", "from", "the", "integration", "tests"])
    values = reader.read("A300:F300")[0]

    assert " ".join(values) == "Hello from the integration tests"

    writer.updateRow(300, ["Goodbye"])
    values = reader.read("A300:F300")[0]

    assert " ".join(values) == "Goodbye from the integration tests"

    writer.updateRow(301, [10, 5, "=A301+B301"])
    values = reader.read("A301:C301")[0]
    assert int(values[2]) == 15

    writer.updateRow(301, [20])
    values = reader.read("A301:C301")[0]
    assert int(values[2]) == 25

def test_append_and_clear(reader, writer):
    writer.appendRow(["this", "was", "appended"])
    values = reader.read("A197:C197")[0]    # Test sheet has a table from 1 to 196
    assert " ".join(values) == "this was appended"
    writer.clear("A197:C197")
    values = reader.read("A197:C197")
    assert len(values) == 0, "Appended row should have been cleared"
