from student import Student
from blocker import Blocker
import pytest

@pytest.mark.skip
def test_blocker(reader):
    
    entries = reader.get_all_entries()

    students = [Student(entry) for entry in entries]

    blocker = Blocker(students)
    
    with open("test_block_file.txt", "w") as outfile:
        blocker.write_block_list_to_file(outfile)
