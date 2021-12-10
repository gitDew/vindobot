class Blocker:
    def __init__(self, students):
        self.students = students

    def write_block_list_to_file(self, outfile):
        if len(self.students) == 0:
            outfile.write("No students received.")
            return
        
        expired_students = [student for student in self.students if student.is_expired() and not student.is_blocked()]

        if len(expired_students) != 0:
            outfile.write("EXPIRED:\n")
            for es in expired_students:
                outfile.write(str(es))

        uncertain_students = [student for student in self.students if student.is_uncertain() and not student.is_blocked()]

        if len(uncertain_students) != 0:
            outfile.write("UNCERTAIN:\n")
            for us in uncertain_students:
                outfile.write(str(us))
