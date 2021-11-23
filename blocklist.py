#!/usr/bin/python3
from gsheets import GoogleSheet
from datetime import datetime

sheet = GoogleSheet()
students = sheet.getStudents()

DATE_FORMAT = "%d.%m.%Y"

def isAlreadyBlocked(student):
    return student["BlockedTill"] and (datetime.strptime(student["BlockedTill"], DATE_FORMAT) > datetime.today())

def isExpired(student):
    return datetime.strptime(student["To"], DATE_FORMAT) < datetime.today()

with open("blocklist.txt", "w") as outfile:
    for student in students.values():
        if isAlreadyBlocked(student):
            continue
        if not student["To"] or isExpired(student):
            line = f'{student["StammNr"]}, {student["FirstName"]} {student["LastName"]}, paid until: {student["To"] if student["To"] else "NA"}'
            if student["Comment"]:
                line += f", Comment: {student['Comment']}"
            outfile.write(line + "\n")

