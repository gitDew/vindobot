from datetime import datetime, date

class Student:
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, entry):
        self.row_id = entry["RowID"]
        self.stamm_nr = entry["StammNr"]
        self.first_name = entry["FirstName"]
        self.last_name = entry["LastName"]
        self.room_nr = entry["RoomNr"]
        self.comment = entry["Comment"]
       

        if entry["BlockedTill"] == "":
            self.blocked_till = ""
        else:
            self.blocked_till = datetime.strptime(entry["BlockedTill"], self.DATE_FORMAT).date()

        if entry["From"] == "":
            self.paid_from = ""
        else:
            self.paid_from = datetime.strptime(entry["From"], self.DATE_FORMAT).date()
        
        if entry["To"] == "":
            self.paid_to = ""
        else:
            self.paid_to = datetime.strptime(entry["To"], self.DATE_FORMAT).date()


    def __str__(self):
        def question_mark_if_empty(attr):
            return attr if attr != "" else "?"

        s = f"{self.stamm_nr}, {self.first_name}, {self.last_name}, Room {question_mark_if_empty(self.room_nr)}."
        if self.paid_to != "":
            s += f" Paid until {self.paid_to.strftime('%d.%m.%Y')}."
        else:
            s += " Paid until ?."
        if self.comment != "":
            s += f" Comment: {self.comment}"
        return s + '\n'

    def is_blocked(self):
        return self.blocked_till != ""

    def is_expired(self):
        return self.paid_to != "" and self.paid_to <= date.today()

    def is_uncertain(self):
        return self.paid_to == ""

