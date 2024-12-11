from django.db import models
from django.contrib.auth.models import User  # This import is needed for the User model, but nothing else from 'models.py' should be imported here.
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.hashers import make_password, check_password  # Correct imports


# Define models without any unnecessary imports

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)  # Unique alphanumeric code for the subject

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    h_t_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    branch = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)  # Hash the password

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # Verify the password hash

    def generate_password(self):
        # Password generation logic
        roll_last_four = self.h_t_no[-4:]
        return f"{roll_last_four}1234"

    def save(self, *args, **kwargs):
        if not self.password:  # Only generate a new password if it's not set
            generated_password = self.generate_password()
            self.set_password(generated_password)  # Hash the generated password
        super().save(*args, **kwargs)  # Don't forget to call the superclass method

    def __str__(self):
        return f"{self.name} ({self.h_t_no})"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link to Student model, not User
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=10)  # "P" for present, "A" for absent
    ip_address = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} on {self.date}"

'''
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link to the student
    roll_number = models.CharField(max_length=20)  # Hall ticket number
    subject_code = models.CharField(max_length=50)  # Subject code
    date = models.DateField(auto_now_add=True)  # Automatically sets the date of attendance

    def __str__(self):
        return f"{self.student.name} - {self.subject_code} - {self.date}"'''

def validate_roll_number(value):
    # Regex pattern to match roll number format like '21AG1A66I1'
    pattern = r'^[0-9]{2}[A-Z]{2}[0-9]{2}[A-Z]{1}[0-9]{1}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid roll number format')
    
#class User(models.Model):
   # username = models.CharField(max_length=100, unique=True) 

    #class Subject(models.Model):
    #code = models.CharField(max_length=100, unique=True)
    #name = models.CharField(max_length=100)
    # other fields related to subjects


class StudentProfile(models.Model):
    Section = models.CharField(max_length=50)
    Branch = models.CharField(max_length=100)
    hall_ticket_number = models.CharField(max_length=20, unique=True)
    student_name = models.CharField(max_length=255)

    def __str__(self):
        return self.student_name

    class Meta:
        db_table = 'attendance_studentprofile'


