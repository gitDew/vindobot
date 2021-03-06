from student import Student
from unittest.mock import patch
from datetime import date
import pytest

@pytest.fixture(scope="module")
def example_students(reader):
    entries = reader.get_all_entries()

    students = []
    for entry in entries:
        students.append(Student(entry))

    return students

def test_converting_entries_to_students(example_students):

    assert len(example_students) == 195     # 195 entries in test sheet
    
    with patch('student.date') as mock_date:
        # assuming it's 2015
        mock_date.today.return_value = date(year=2015, month=1, day=10)
        blocked_students = [student for student in example_students if student.is_blocked()]
    assert len(blocked_students) == 18  # 18 blocked students in test sheet

def test_given_everyone_expired_or_uncertain(example_students):
    with patch('student.date') as mock_date:
        # assuming it's 2030
        mock_date.today.return_value = date(year=2030, month=2, day=10)
        expired_students = [student for student in example_students if student.is_expired()]
        uncertain_students = [student for student in example_students if student.is_uncertain()]
        assert len(expired_students) == 165     # 165 expired students in test sheet
        assert len(uncertain_students) == 30     # 30 uncertain students in test sheet
        

def test_given_everyone_paid_except_empty(example_students):
    with patch('student.date') as mock_date:
        # assuming it's 1997
        mock_date.today.return_value = date(year=1997, month=2, day=10)
        expired_students = [student for student in example_students if student.is_expired()]
        
        for expired_student in expired_students:
            assert expired_student.paid_to == ""
