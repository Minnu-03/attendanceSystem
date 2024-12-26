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


