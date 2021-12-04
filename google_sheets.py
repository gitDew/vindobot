import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def authenticate():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

class RequestFactory:
    def __init__(self, sheet_values_obj, spreadsheet_ID):
        self.sheet_values_obj = sheet_values_obj
        self.spreadsheet_ID = spreadsheet_ID
    
    def build_get_request(self, range):
        return self.sheet_values_obj.get(spreadsheetId=self.spreadsheet_ID,\
                range=range)

    def build_update_request(self, range, body):
        return self.sheet_values_obj.update(spreadsheetId=self.spreadsheet_ID,\
                range=range, valueInputOption="USER_ENTERED", body=body)

    def build_clear_request(self, range):
        return self.sheet_values_obj.clear(spreadsheetId=self.spreadsheet_ID, \
                range=range)

    def build_append_request(self, range, body):
        return self.sheet_values_obj.append(spreadsheetId=self.spreadsheet_ID,\
                range=range, insertDataOption="INSERT_ROWS",\
                valueInputOption="USER_ENTERED", body=body)

class Reader:
    KEYS = ["StammNr", "FirstName", "LastName", "RoomNr", "BlockedTill", "From", "To", "Comment"]
    FULL_RANGE = 'students!A:H' 
    
    def __init__(self, request_factory):
        self.request_factory = request_factory

    def getAllEntries(self):
        entries = []
        rows = self.read(self.FULL_RANGE)[1:]
        
        for rowID, row in enumerate(rows, 2):
            entry = {k: "" for k in self.KEYS}
            entry["RowID"] = rowID
            for k, v in zip(self.KEYS, row):
                entry[k] = v
            
            entries.append(entry)

        return entries

    def read(self, range):
        request = self.request_factory.build_get_request(range)
        result = request.execute()
        return result.get('values', [])

class Writer:
    TABLE_AT = "A1"

    def __init__(self, request_factory):
        self.request_factory = request_factory 
        
    def updateRow(self, rowID, values):
        body = {
            'values': [values] 
        }

        range = "students!A" + str(rowID)
        request = self.request_factory.build_update_request(range, body)
        result = request.execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))
    
    def clear(self, range):
        request = self.request_factory.build_clear_request(range)
        result = request.execute()
        print(f"{range} cleared.")

    def appendRow(self, values):
        body = {
                'values': [values]
                }
        range = self.TABLE_AT 
        request = self.request_factory.build_append_request(range, body)
        result = request.execute()
        print('Row appended.')
    
