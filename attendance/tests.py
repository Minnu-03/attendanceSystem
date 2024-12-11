from django.test import TestCase
from .models import Student

class StudentTestCase(TestCase):
    def test_student_password_generation(self):
        student = Student.objects.create(
            h_t_no="21AG1A66I1",
            name="John Doe",
            section="A",
            branch="Science"
        )
        # Check if password was generated correctly
        expected_password = "66I11234"
        self.assertTrue(student.check_password(expected_password))


# Test reading the CSV file
import csv

csv_filename = "/path/to/your/csv/2022_CSM_Students.csv"
try:
    with open(csv_filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)  # Just to see if it reads without error
except UnicodeDecodeError:
    print("Unicode decode error encountered.")
except Exception as e:
    print(f"An error occurred: {e}")
