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

    def is_blocked(self):
        return self.blocked_till != ""

    def is_expired(self):
        return self.paid_to == "" or self.paid_to <= date.today()

