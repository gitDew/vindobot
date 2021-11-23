#!/usr/bin/python3

from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json

class GoogleSheet:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    FULL_RANGE = 'students!A:H' 
    KEYS = ["StammNr", "FirstName", "LastName", "RoomNr", "BlockedTill", "From", "To", "Comment"]

    def __init__(self):
        with open('mycreds.json') as credsfile:
            mycreds = json.load(credsfile)
            self.SPREADSHEET_ID = mycreds["spreadsheetID"]

        creds = self.authenticate()
        service = build('sheets', 'v4', credentials=creds) 
        self.sheet = service.spreadsheets()
    
    def getStudents(self):
        students = {}
        rows = self._getSheet()[1:]
        
        for rowID, row in enumerate(rows, 2):
            student = {k: "" for k in self.KEYS}
            student["RowID"] = rowID
            for k, v in zip(self.KEYS, row):
                student[k] = v
            
            students[row[0]] = student

        return students 

    def _getSheet(self):
        result = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID,
                range=self.FULL_RANGE).execute()
        return result.get('values', [])
    
    def updateRow(self, rowID, values):
        body = {
            'values': [values] 
        }

        range = "students!A" + rowID
        result = self.sheet.values().update(
            spreadsheetId=self.SPREADSHEET_ID, range=range,
            valueInputOption="USER_ENTERED", body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))

    def appendRow(self, values):
        body = {
                'values': [values]
                }
        
        self.sheet.values().append(
                spreadsheetId=self.SPREADSHEET_ID, range="A1",
                insertDataOption="INSERT_ROWS", valueInputOption="USER_ENTERED", body=body
                ).execute()
        print('Row appended.')
    def authenticate(self):
        creds = None

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds
