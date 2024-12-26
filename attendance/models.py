#for db models
from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.hashers import make_password, check_password  
from django.contrib import admin


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    h_t_no = models.CharField(max_length=20, unique=True)  
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    branch = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.h_t_no})"



class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=10)  # "P" for present, "A" for absent
    ip_address = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} on {self.date}"

def validate_roll_number(value):
    # Regex pattern to match roll number format like '21AG1A66I1'
    pattern = r'^[0-9]{2}[A-Z]{2}[0-9]{2}[A-Z]{1}[0-9]{1}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid roll number format')
    


class StudentProfile(models.Model):
    Section = models.CharField(max_length=50)
    Branch = models.CharField(max_length=100)
    hall_ticket_number = models.CharField(max_length=20, unique=True)
    student_name = models.CharField(max_length=255)

    def __str__(self):
        return self.student_name

    class Meta:
        db_table = 'attendance_studentprofile'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code') 