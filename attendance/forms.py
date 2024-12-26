from django import forms
from .models import Student
from django.contrib.auth.forms import AuthenticationForm


#For forms
#For authentication
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'password']

class TeacherLoginForm(AuthenticationForm):
    # can add custom fields here if needed
    pass