from django.contrib import admin
from .models import Student, Subject, Attendance
from .models import StudentProfile

# Registering the Student model with a custom admin interface
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'branch', 'h_t_no')  # Customize which fields to display in the admin list

# Registering the Attendance model
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'ip_address')  # Customize which fields to display in the admin list
    list_filter = ('subject', 'date')  # Add filters for subject and date
    search_fields = ('student__name', 'subject__name')  # Add search functionality


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'Section', 'Branch', 'hall_ticket_number']
