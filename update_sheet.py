#!/usr/bin/env python3
import csv
from gsheets import GoogleSheet

changes = {}

sheet = GoogleSheet()
students = sheet.getStudents()
new_students = []
# TODO: download entry automatically

with open('workitout_list.csv', 'r') as workitoutfile:
    workitout_reader = csv.DictReader(workitoutfile)

    for entry in workitout_reader:
        if entry["StammNr"] not in students:
            new_students.append(list(entry.values()))
            continue

        student = students[entry["StammNr"]]
       
        if all(student[key] == entry[key] for key in entry.keys()):
            continue
        
        changes[student["StammNr"]] = [entry[key] if entry[key] != student[key] else None for key in entry.keys()]

for new_student in new_students:
    sheet.appendRow(new_student)

for k, v in changes.items():
    rowID = str(students[k]['RowID'])
    sheet.updateRow(rowID, v)

