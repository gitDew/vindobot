import pytest
from unittest.mock import patch
from datetime import date
from student import Student

def test_student_has_the_right_attributes(paying_example_student):
    assert paying_example_student.row_id == 9
    assert paying_example_student.stamm_nr == "123456"
    assert paying_example_student.first_name == "Martin"
    assert paying_example_student.last_name == "Scorsese"
    assert paying_example_student.room_nr == "987"
    assert paying_example_student.blocked_till == ""
    assert paying_example_student.paid_from == date(year=2021, month=1, day=1)
    assert paying_example_student.paid_to == date(year=2021, month=4, day=1)
    assert paying_example_student.comment == "Shutter Island was great"

def test_given_student_who_paid_should_not_be_blocked(paying_example_student):
    assert not paying_example_student.is_blocked()

def test_blocked_student_should_be_blocked(blocked_example_student):
    assert blocked_example_student.is_blocked()

def test_is_expired(expired_but_not_blocked_example_student, paying_example_student):
    with patch('student.date') as mock_date:
        # assuming today is the 10th of February 2021
        mock_date.today.return_value = date(year=2021, month=2, day=10)
        assert expired_but_not_blocked_example_student.is_expired()
        assert not paying_example_student.is_expired()

def test_expired_for(expired_but_not_blocked_example_student):
    with patch('student.date') as mock_date:
        # assuming today is the 10th of February 2021
        mock_date.today.return_value = date(year=2021, month=2, day=10)
        assert expired_but_not_blocked_example_student.expired_for() == 5

def test_uncertain(uncertain_example_student):
    assert not uncertain_example_student.is_blocked(), "Empty BlockedTill should not be seen as blocked"
    assert not uncertain_example_student.is_expired(), "Empty to fields should not be seen as expired"
    assert uncertain_example_student.is_uncertain(), "Empty to field should be seen as being uncertain"

def test_given_invalid_blocked_throws_exception():
    student_entry = {"RowID": 12, "StammNr": "123459", "FirstName": "Joe", "LastName": "Rotten", 
            "RoomNr": "987", "BlockedTill": "??????", "From": "", "To": "", "Comment": ""}
     
    with pytest.raises(ValueError):
        Student(student_entry)

def test_given_invalid_from_throws_exception():
    student_entry = {"RowID": 12, "StammNr": "123459", "FirstName": "Joe", "LastName": "Rotten", 
            "RoomNr": "987", "BlockedTill": "", "From": "12.02.2022?", "To": "", "Comment": ""}
     
    with pytest.raises(ValueError):
        Student(student_entry)

def test_given_invalid_to_throws_exception():
    student_entry = {"RowID": 12, "StammNr": "123459", "FirstName": "Joe", "LastName": "Rotten", 
            "RoomNr": "987", "BlockedTill": "", "From": "", "To": "11.11.2022?????????", "Comment": ""}
     
    with pytest.raises(ValueError):
        Student(student_entry)
