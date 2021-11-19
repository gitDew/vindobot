#!/usr/bin/python3
import csv
from gsheets import GoogleSheet

keys = ["StammNr", "PreName", "Name", "Zimmernummer", "BlockedTill"]
changes = {}

sheet = GoogleSheet()
students = sheet.getStudents()
new_students = []
# TODO: download entry automatically
with open('workitout_list.csv', 'r') as workitoutfile:
    workitout_reader = csv.DictReader(workitoutfile)

    for entry in workitout_reader:

        # remove redundant 00:00:00 time from date
        entry["BlockedTill"], _ = entry["BlockedTill"].split()

        if entry["StammNr"] not in students:
            new_students.append([entry[key] for key in keys])
            continue

        student = students[entry["StammNr"]]
       
        if all(student[key] == entry[key] for key in keys):
            continue
        
        changes[student["StammNr"]] = [entry[key] if entry[key] != student[key] else None for key in keys ]

for new_student in new_students:
    sheet.appendRow(new_student)

for k, v in changes.items():
    rowID = str(students[k]['rowID'])
    sheet.updateRow(rowID, v)



