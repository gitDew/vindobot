#!/usr/bin/env python3

import google_sheets
from credentials import MyCredentials
from student import Student
from blocker import Blocker
from chromedriver_py import binary_path
from googleapiclient.discovery import build
from selenium import webdriver
import workitout
import csv

spreadsheet_ID = "16p4zH-z6z2ggr86Vmson9mlroWhWE85zECgryrv2Vno" 

creds = google_sheets.authenticate()
service = build('sheets', 'v4', credentials=creds)
sheet_values_obj = service.spreadsheets().values()

request_factory = google_sheets.RequestFactory(sheet_values_obj, spreadsheet_ID)
greader = google_sheets.Reader(request_factory, "Heimbewohner Liste")

credentials = MyCredentials()
mycreds = credentials.get_credentials()

driver = webdriver.Chrome(executable_path=binary_path)
auth = workitout.Authenticator(mycreds["url"], driver)    
cookie = auth.login_for_cookies(mycreds["username"], mycreds["password"])
fetcher = workitout.Fetcher(mycreds["data_url"], cookie)
workitout_students = fetcher.fetch()

entries = greader.get_all_entries()

gstudents = {} 

for entry in entries:
    gstudents[entry["FirstName"] + " " + entry["LastName"]] = entry

for wstudent in workitout_students:
    wstudent["From"] = ""
    wstudent["To"] = ""
    wstudent["Comment"] = ""

    full_name = wstudent["FirstName"] + " " +  wstudent["LastName"]

    if full_name in gstudents:
        gstudent = gstudents[full_name]
        wstudent["From"] = gstudent["From"]
        wstudent["To"] = gstudent["To"]
        wstudent["Comment"] = gstudent["Comment"]

with open('merged.csv', 'w') as f:
    w = csv.DictWriter(f, ["StammNr", "FirstName", "LastName", "RoomNr", "BlockedTill", "From", "To", "Comment"])
    w.writeheader()
    w.writerows(workitout_students)
