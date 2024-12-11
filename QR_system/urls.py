# QR_system/urls.py

from django.contrib import admin
from django.urls import path, include  # Keep the include import
# Import views from the 'attendance' app
from attendance import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('attendance/', include('attendance.urls')),  # This includes the attendance app URLs
    path('login/', views.student_login, name='student_login'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('', views.home, name='home'),
]
