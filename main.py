#!/usr/bin/env python3

import google_sheets
from credentials import MyCredentials
from student import Student
from blocker import Blocker
from updater import Updater

from chromedriver_py import binary_path
from googleapiclient.discovery import build
from selenium import webdriver
import workitout

spreadsheet_ID = "16p4zH-z6z2ggr86Vmson9mlroWhWE85zECgryrv2Vno" 

creds = google_sheets.authenticate()
service = build('sheets', 'v4', credentials=creds)
sheet_values_obj = service.spreadsheets().values()

request_factory = google_sheets.RequestFactory(sheet_values_obj, spreadsheet_ID)
greader = google_sheets.Reader(request_factory, "Heimbewohner Liste")
gwriter = google_sheets.Writer(request_factory, "Heimbewohner Liste")

credentials = MyCredentials()
mycreds = credentials.get_credentials()

driver = webdriver.Chrome(executable_path=binary_path)
auth = workitout.Authenticator(mycreds["url"], driver)    
cookie = auth.login_for_cookies(mycreds["username"], mycreds["password"])
fetcher = workitout.Fetcher(mycreds["data_url"], cookie)
workitout_students = fetcher.fetch()


updater = Updater(fetcher, greader, gwriter)
changes, new = updater.diff()

updater.update(changes)
updater.add(new)

entries = greader.get_all_entries()
gstudents = []
for entry in entries:
    gstudents.append(Student(entry))

blocker = Blocker(gstudents)

with open("blocklist.txt", "w") as f:
    blocker.write_block_list_to_file(f)
