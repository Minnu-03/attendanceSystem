from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Custom URLs
    path('generate-qr/', views.generate_qr, name='generate_qr'),
    path('teacher-login/', views.teacher_login, name='teacher_login'),
    path('student-login/', views.student_login, name='student_login'),  # Custom student login view
    path('', views.home, name='home'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('submit_attendance/', views.submit_attendance, name='submit_attendance'),
    path('update_student_details/', views.student_dashboard, name='update_student_details'),
    path('profiles/', views.display_student_profiles, name='display_student_profiles'),
    path('attendance-details/', views.attendance_details, name='attendance_details'),
    path('attendance_form/', views.attendance_form, name='attendance_form'),

    # Django built-in login/logout views (use whichever you prefer, not both)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Default login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
