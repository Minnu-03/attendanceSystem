from django import forms
from .models import Student  # This is fine as long as it's in the QR_system folder
from django.contrib.auth.forms import AuthenticationForm

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'password']

class TeacherLoginForm(AuthenticationForm):
    # You can add custom fields here if needed
    pass