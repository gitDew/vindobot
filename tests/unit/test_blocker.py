import pytest
from blocker import Blocker
from io import StringIO
from unittest.mock import patch
from datetime import date

@pytest.fixture
def outfile():
    outfile = StringIO()
    yield outfile
    outfile.close()

def test_given_empty_students_blocker_writes_no_students(outfile):
    students = []

    blocker = Blocker(students)

    blocker.write_block_list_to_file(outfile)

    value = outfile.getvalue()

    assert value == "No students received."

def test_given_expired_student_appears_in_block_list(expired_but_not_blocked_example_student, outfile):
    students = [expired_but_not_blocked_example_student]

    blocker = Blocker(students)

    blocker.write_block_list_to_file(outfile)
    value = outfile.getvalue()

    assert value == "EXPIRED:\n123458, Sneaky, Man, Room 667. Paid until 05.02.2021. Comment: Careful, this guy is sneaky\n"

def test_given_expired_student_without_comment_appears_without_comment(expired_but_not_blocked_example_student, outfile):
    expired_but_not_blocked_example_student.comment = ""
    students = [expired_but_not_blocked_example_student]

    blocker = Blocker(students)

    blocker.write_block_list_to_file(outfile)
    value = outfile.getvalue()

    assert value == "EXPIRED:\n123458, Sneaky, Man, Room 667. Paid until 05.02.2021.\n"

def test_given_paying_and_expired_student_only_expired_appears(paying_example_student, expired_but_not_blocked_example_student, outfile):
    students = [paying_example_student, expired_but_not_blocked_example_student]

    blocker = Blocker(students)

    with patch('student.date') as mock_date:
        # assuming today is the 10th of February 2021
        mock_date.today.return_value = date(year=2021, month=2, day=10)
        blocker.write_block_list_to_file(outfile)

    value = outfile.getvalue()

    assert value == "EXPIRED:\n123458, Sneaky, Man, Room 667. Paid until 05.02.2021. Comment: Careful, this guy is sneaky\n"

def test_given_uncertain_student_only_uncertain_appears(uncertain_example_student, outfile):
    students = [uncertain_example_student]

    blocker = Blocker(students)

    blocker.write_block_list_to_file(outfile)

    value = outfile.getvalue()
    
    assert value == "UNCERTAIN:\n123459, Johnny, Uncertain, Room ?. Paid until ?. Comment: ?\n"

def test_given_expired_and_uncertain_both_appear(expired_but_not_blocked_example_student, uncertain_example_student, outfile):
    students = [expired_but_not_blocked_example_student, uncertain_example_student]
    
    blocker = Blocker(students)

    blocker.write_block_list_to_file(outfile)

    value = outfile.getvalue()
    assert value == "EXPIRED:\n123458, Sneaky, Man, Room 667. Paid until 05.02.2021. Comment: Careful, this guy is sneaky\nUNCERTAIN:\n123459, Johnny, Uncertain, Room ?. Paid until ?. Comment: ?\n"

def test_given_blocked_does_not_appear(blocked_example_student, outfile):
    students = [blocked_example_student]

    blocker = Blocker(students)

    blocker.write_block_list_to_file(outfile)

    value = outfile.getvalue()

    assert value == ""

def test_given_uncertain_but_blocked_does_not_appear(uncertain_blocked_example_student, outfile):
    students = [uncertain_blocked_example_student]

    blocker = Blocker(students)
    blocker.write_block_list_to_file(outfile)
    value = outfile.getvalue()

    assert value == ""
