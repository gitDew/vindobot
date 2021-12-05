
class Updater:
    
    def __init__(self, workitout_fetcher, google_reader, google_writer):
        self.workitout_fetcher = workitout_fetcher
        self.google_reader = google_reader
        self.google_writer = google_writer
    
    def diff(self):
        changes = []
        new = []

        wi_students = self.workitout_fetcher.fetch()
        g_entries = self.google_reader.getAllEntries()
        
        by_stamm_nr = {student["StammNr"]: student for student in g_entries} 

        for wi_student in wi_students:
            student_changes = []
            if wi_student["StammNr"] not in by_stamm_nr:
                # new student who is not in sheets yet
                new.append(wi_student) 
                continue
            entry = by_stamm_nr[wi_student["StammNr"]]
            
            for key in wi_student.keys():
                if wi_student[key] != entry[key]:
                    student_changes.append(wi_student[key])
                else:
                    student_changes.append(None)
            if any(student_changes):
                changes.append({"RowID": entry["RowID"], "diff": student_changes})
        return changes, new
    
    def add(self, new):
        for new_student in new:
            self.google_writer.appendRow([new_student["StammNr"], new_student["FirstName"], new_student["LastName"], new_student["RoomNr"], new_student["BlockedTill"]])

    def update(self, changes):
        for change in changes:
            self.google_writer.updateRow(change["RowID"], change["diff"])
