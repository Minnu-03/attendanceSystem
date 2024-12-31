import qrcode
import io
import base64
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from .models import Subject, Attendance,Student
from .forms import TeacherLoginForm
from django.contrib.auth import authenticate, login 
from django.http import HttpResponse
import os
from django.conf import settings
from django.contrib.auth.models import User  # Correct import for User model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
import socket
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt 
from .models import StudentProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import Attendance
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.urls import reverse
from django.utils.timezone import now

# Render the attendance form

def generate_qr(request):
    qr_code_url = None

    if request.method == 'POST':
        subject_code = request.POST.get('subject_id')  # Subject ID from form
        try:
            subject = Subject.objects.get(code=subject_code)
        except Subject.DoesNotExist:
            return HttpResponse("Invalid Subject Code.", status=400)

        # Use the Ngrok public URL (replace this manually if needed)
        #Change url here
        ngrok_url = "https://92fe-2401-4900-5085-7343-f0c6-de50-7c94-9ac8.ngrok-free.app"  # Replace with your actual Ngrok public URL
        qr_data = f"{ngrok_url}{reverse('student_login')}?subject_id={subject.code}"

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert the image to base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        qr_code_url = f"data:image/png;base64,{qr_code_base64}"

    return render(request, 'generate_qr_code.html', {'qr_code': qr_code_url})


def home(request):
    return render(request, 'home.html')  # Display home page with options

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Attempting to log in user: {username}")  # Debugging line

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            print(f"Login successful for {username}")  # Debugging line
            return redirect('generate_qr')
        else:
            print("Invalid credentials or not authorized.")  # Debugging line
            return HttpResponse("Invalid credentials or not authorized.", status=401)

    return render(request, 'teacher_login.html')

@csrf_protect
def submit_attendance(request):
    if request.method == 'POST':
        # Handle the POST request here
        pass


def mark_attendance(request):
    if request.method == 'POST':
        student_name = request.POST.get('name')
        subject_code = request.POST.get('subject_id')
        timestamp = request.POST.get('timestamp')

        # Fetch the subject using subject_code
        try:
            subject = Subject.objects.get(code=subject_code)
        except Subject.DoesNotExist:
            return JsonResponse({'error': 'Invalid subject code'}, status=400)

        # Fetch the student based on the name
        student = User.objects.filter(username=student_name).first()

        if not student:
            return JsonResponse({'error': 'Student not found'}, status=404)

        # Capture the student's IP address
        ip_address = request.META.get('REMOTE_ADDR')

        # Mark attendance as "P" (Present)
        attendance = Attendance.objects.create(
            student=student,
            subject=subject,
            date=timestamp,  # Use the timestamp from the QR code
            status="P",  # Mark as "Present"
            ip_address=ip_address  # Record the student's IP address
        )

        return JsonResponse({'message': 'Attendance marked successfully'}, status=200)

    return render(request, 'mark_attendance.html')


def home(request):
    return render(request, 'home.html')  # Display home page with options

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Attempting to log in user: {username}")  # Debugging line

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            print(f"Login successful for {username}")  # Debugging line
            return redirect('generate_qr')
        else:
            print("Invalid credentials or not authorized.")  # Debugging line
            return HttpResponse("Invalid credentials or not authorized.", status=401)

    return render(request, 'teacher_login.html')


@csrf_protect
def student_login(request):
    error_message = None  # Variable to store any error messages

    if request.method == 'POST':
        h_t_no = request.POST.get('h_t_no')  # Hall Ticket Number
        password = request.POST.get('password')  # Password entered by the student

        print(f"Entered Hall Ticket Number: {h_t_no}")  # Debugging: Print entered Roll Number
        print(f"Entered Password: {password}")  # Debugging: Print entered Password

        try:
            # Fetch the student based on the Hall Ticket Number (h_t_no)
            student = Student.objects.get(h_t_no=h_t_no)
            print(f"Found Student: {student.name}")  # Debugging: Student found

            # Check if the entered password matches the stored hashed password
            if student.check_password(password):
                print("Password is correct!")  # Debugging: Password match
                request.session['h_t_no'] = student.h_t_no  # Store h_t_no in session
                return redirect('attendance_form')  # Redirect to attendance form
            else:
                error_message = "Incorrect password."
                print("Incorrect password.")  # Debugging: Password mismatch
        except Student.DoesNotExist:
            error_message = "Student not found."
            print("Student not found.")  # Debugging: No student with the entered h_t_no

    # If the method is GET, or if there are errors, render the login form
    return render(request, 'student_login.html')

def attendance_form(request):
   """
   This view handles the attendance form submission for a logged-in student.
   It checks if the student is logged in and allows them to submit their attendance.
   """
   # Get the student's Hall Ticket Number from the session
   h_t_no = request.session.get('h_t_no')  # Retrieve h_t_no from session


   if not h_t_no:
       # If the student is not logged in (session does not have 'h_t_no')
       return redirect('student_login')  # Redirect to login if student is not logged in


   try:
       # Get the student object using the hall ticket number
       student = Student.objects.get(h_t_no=h_t_no)
       print(f"Student found: {student.name}")
       print(request.method )
   except Student.DoesNotExist:
       # Handles the case if no student is found for the provided hall ticket number
       print("Student not found.")
       return redirect('student_login')


   if request.method == 'POST':
       # Gets values from the form
       subject_code = request.POST.get('subject')  # Subject


       # Save the attendance in the database
       attendance = Attendance(
           student=student,  # Assign the logged-in student
           roll_number=h_t_no,  # Roll number from the form
           subject_code=subject_code,  # Subject from the form
       )
       attendance.save()  # Saves the attendance record to the database


       print(f"Attendance Submitted: {h_t_no}, {subject_code}")
      
       return redirect('attendance_details')


   return render(request, 'attendance/attendance_form.html', {'student': student})


def submit_attendance(request):
    print(f"Request Method: {request.method}")
    print(f"POST Data: {request.POST}")
    if request.method == 'POST':
        # Debugging: Log the POST data
        print(f"POST Data Received: {request.POST}")

        student_name = request.POST.get('name')  # The student's name
        roll_number = request.POST.get('h_t_no')  # Roll number (hall ticket number)
        subject_code = request.POST.get('subject')  # Subject code

        # Validate form data
        if not student_name or not roll_number or not subject_code:
            print("Error: Missing required fields")
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

        # Fetch the student record
        try:
            student = Student.objects.get(name=student_name, h_t_no=roll_number)
            print(f"Student Found: {student}")
        except Student.DoesNotExist:
            print("Error: Student not found")
            return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)

        # Fetch the subject record
        try:
            subject = Subject.objects.get(code=subject_code)
            print(f"Subject Found: {subject}")
        except Subject.DoesNotExist:
            print("Error: Subject not found")
            return JsonResponse({'status': 'error', 'message': 'Invalid subject code'}, status=400)

        # Mark attendance
        try:
            ip_address = request.META.get('REMOTE_ADDR', 'Unknown')  # Get the client's IP address
            attendance = Attendance.objects.create(
                student=student,
                subject=subject,
                date=now(),  # Using the current timestamp
                status="P",  # Marking as "Present"
                ip_address=ip_address
            )
            print(f"Attendance Created Successfully: {attendance}")
        except Exception as e:
            print(f"Error while creating attendance: {e}")
            return JsonResponse({'status': 'error', 'message': 'Failed to mark attendance'}, status=500)

        # Return a success response
        return JsonResponse({'status': 'success', 'message': 'Attendance marked successfully'}, status=200)

    # Render the attendance form for GET requests
    return render(request, 'attendance_form.html')


def attendance_details(request):
    # Get the logged-in student's attendance details
    student = request.user  # Assuming the user is a logged-in student
    print('getting ttendnace details')

    # Fetch attendance for the logged-in student (you can customize this query)
    attendance_records = Attendance.objects.filter(student=student)

    return render(request, 'attendance_details.html', {
        'attendance_records': attendance_records
    })

@login_required
def student_dashboard(request):
    # Fetch the student's information from the session or database
    student = Student.objects.get(user=request.user)  # Assuming a User model is linked to Student
    print(f'updating dashboard for {student}')

    if request.method == 'POST':
        # Update details form
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        student.email = email
        student.phone_number = phone_number
        student.save()

        # Optionally, show a success message
        return render(request, 'student_dashboard.html', {'student': student, 'success': 'Details updated successfully.'})

    return render(request, 'student_dashboard.html', {'student': student})


def display_student_profiles(request):
    profiles = StudentProfile.objects.all()
    return render(request, 'attendance/display_profiles.html', {'profiles': profiles})


def verify_student_password(h_t_no, password):
    try:
        # Fetch the student from the database by Hall Ticket Number (h_t_no)
        student = Student.objects.get(h_t_no=h_t_no)

        # Check if the entered password matches the stored hashed password
        if check_password(password, student.password):
            print("Password is correct!")
        else:
            print("Incorrect password.")
    except Student.DoesNotExist:
        print("Student not found.")


def login_view(request):
    h_t_no = request.POST['h_t_no']
    entered_password = request.POST['password']
    
    # Retrieve student by hall ticket number
    try:
        student = Student.objects.get(h_t_no=h_t_no)
    except Student.DoesNotExist:
        return render(request, 'login.html', {'error': 'Student not found'})

    # Compare the entered password with the stored password (assuming it's hashed)
    if check_password(entered_password, student.password):
        # Password is correct, log the student in
        return redirect('student_dashboard')  # Redirect to the dashboard or homepage
    else:
        return render(request, 'login.html', {'error': 'Incorrect password'})
    
