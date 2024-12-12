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
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt 
from .models import StudentProfile
from django.contrib.auth.models import User
from .models import Attendance
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.utils import timezone


def generate_qr(request):
    qr_code_url = None  # Default to None if no QR code is generated

    if request.method == 'POST':
        subject_code = request.POST.get('subject_id')  # Get subject ID (e.g., 'ai101')

        # Validate if subject exists using subject_code
        try:
            subject = Subject.objects.get(code=subject_code)  # Query by subject code
        except Subject.DoesNotExist:
            return HttpResponse("Invalid Subject Code.", status=400)

        # **Dynamically Fetch Local IP Address**
        local_ip = socket.gethostbyname(socket.gethostname())  # Get the local IP address
        # Generate the URL with the correct local IP
        qr_data = f"http://{local_ip}:8000/login/?subject_id={subject.code}"

        # Print the QR code data (for debugging)
        print(f"QR Code URL: {qr_data}")

        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert the QR code image to base64 and prepare it for display
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Convert the image buffer to base64
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        qr_code_url = f"data:image/png;base64,{qr_code_base64}"  # Set the base64-encoded image data

    return render(request, 'generate_qr_code.html', {'qr_code': qr_code_url})


# Home page (simple)
def home(request):
    return render(request, 'home.html')


# Mark Attendance (when student scans the QR Code)
# attendance/views.py

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


'''def student_login(request):
    if request.method == 'POST':
        # Get student data from the form
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            # Fetch the student using the name
            student = Student.objects.get(name=name)
            #print(student.password,password,student.password==password,check_password(password, student.password))

            # Check if the entered password matches the stored hashed password
            if check_password(password, student.password):
                # If password is correct, store session data and redirect to attendance form
                request.session['name'] = student.name
                return redirect('attendance_form')  # Redirect to the attendance form
            else:
                # If password doesn't match
                return render(request, 'student_login.html', {'error': 'Invalid password or student name.'})

        except Student.DoesNotExist:
            # If the student doesn't exist
            return render(request, 'student_login.html', {'error': 'Student not found.'})

    return render(request, 'student_login.html')'''


'''def student_login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(name=name, password=password)
            request.session['name'] = student.name
            # Check if subject_id exists in the URL and store it in session
            subject_id = request.GET.get('subject_id')
            if subject_id:
                request.session['subject_id'] = subject_id
            return redirect('attendance_form')  # Redirect to the attendance form after login
        except Student.DoesNotExist:
            return HttpResponse("Invalid credentials", status=400)

    return render(request, 'student_login.html')'''

@csrf_protect
def submit_attendance(request):
    if request.method == 'POST':
        # Handle the POST request here
        pass

def generate_qr(request):
    qr_code_url = None  # Default to None if no QR code is generated

    if request.method == 'POST':
        subject_code = request.POST.get('subject_id')  # Get subject ID (e.g., 'ai101')

        # Validate if subject exists using subject_code
        try:
            subject = Subject.objects.get(code=subject_code)  # Query by subject code
        except Subject.DoesNotExist:
            return HttpResponse("Invalid Subject Code.", status=400)

        # **Dynamically Fetch Local IP Address**
        local_ip = socket.gethostbyname(socket.gethostname())  # Get the local IP address
        # Generate the URL with the correct local IP
        qr_data = f"http://{local_ip}:8000/login/?subject_id={subject.code}"

        # Print the QR code data (for debugging)
        print(f"QR Code URL: {qr_data}")

        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert the QR code image to base64 and prepare it for display
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Convert the image buffer to base64
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        qr_code_url = f"data:image/png;base64,{qr_code_base64}"  # Set the base64-encoded image data

    return render(request, 'generate_qr_code.html', {'qr_code': qr_code_url})


# Home page (simple)
def home(request):
    return render(request, 'home.html')


# Mark Attendance (when student scans the QR Code)
# attendance/views.py

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
        h_t_no = request.POST.get('h_t_no')  # Roll Number / Hall Ticket Number
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
    except Student.DoesNotExist:
        # Handle the case if no student is found for the provided hall ticket number
        print("Student not found.")
        return redirect('student_login')

    if request.method == 'POST':
        # Get the values from the form
        subject_code = request.POST.get('subject')  # Subject

        # Save the attendance in the database
        attendance = Attendance(
            student=student,  # Assign the logged-in student
            roll_number=h_t_no,  # Roll number from the form
            subject_code=subject_code,  # Subject from the form
        )
        attendance.save()  # Save the attendance record to the database

        print(f"Attendance Submitted: {h_t_no}, {subject_code}")
        
        # Redirect to the attendance details page after submitting
        return redirect('attendance_details')

    # Render the attendance form template with the student's data
    return render(request, 'attendance/attendance_form.html', {'student': student})


@login_required
def submit_attendance(request):
    if request.method == 'POST':
        student = request.user  # Assuming user is linked to the Student model
        h_t_no = request.POST['h_t_no']
        subject_code = request.POST['subject']

        try:
            subject = Subject.objects.get(code=subject_code)
        except Subject.DoesNotExist:
            return JsonResponse({'error': 'Invalid subject code'}, status=400)

        # Create Attendance record
        attendance = Attendance.objects.create(
            student=student,
            subject=subject,
            status='P'  # or other status like 'A' for absent
        )

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)




@login_required
def student_dashboard(request):
    # Fetch the student's information from the session or database
    student = Student.objects.get(user=request.user)  # Assuming a User model is linked to Student

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

@login_required
def submit_attendance(request):
    if request.method == 'POST':
        # Submit attendance form
        student_name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')
        subject = request.POST.get('subject')

        # Logic to save the attendance, for example:
        student = Student.objects.get(name=student_name, roll_number=roll_number)
        # Create attendance record (assuming an Attendance model exists)
        # Attendance.objects.create(student=student, subject=subject)

        return redirect('student_dashboard')  # Redirect back to the student dashboard or another page

    return render(request, 'attendance_form.html')  # If not a POST request, show the form


@login_required
def my_view(request):
    # Your view logic
    return render(request, 'my_template.html')


def display_student_profiles(request):
    profiles = StudentProfile.objects.all()
    return render(request, 'attendance/display_profiles.html', {'profiles': profiles})


def generate_passwords_for_students(request):
    # This view will generate passwords for all students in the database
    students = Student.objects.all()
    for student in students:
        if not student.password:  # Only generate password if not already set
            student.save()  # This will trigger the save method and generate password

    return render(request, 'student_passwords_generated.html', {'students': students})

def create_student_user(student):
    # Create a new user, using the student's hall ticket number as the username and generating a password
    user = User.objects.create_user(username=student.h_t_no, password=student.generate_password())
    
    # Use the student's full name as the first name and leave the last name as an empty string
    user.first_name = student.name  # Set full name as the first name
    user.last_name = ''  # Leave last name empty
    user.save()
    
    return user


def attendance_details(request):
    # Get the logged-in student's attendance details
    student = request.user  # Assuming the user is a logged-in student

    # Fetch attendance for the logged-in student (you can customize this query)
    attendance_records = Attendance.objects.filter(student=student)

    return render(request, 'attendance_details.html', {
        'attendance_records': attendance_records
    })


@csrf_exempt
def submit_attendance(request):
    if request.method == 'POST':
        # Get the data from the POST request
        student_name = request.POST.get('name')  # The student name
        subject_code = request.POST.get('subject')  # The subject code
        timestamp = request.POST.get('timestamp')  # The timestamp from the QR code

        # Fetch the subject using the subject code
        try:
            subject = Subject.objects.get(code=subject_code)
        except Subject.DoesNotExist:
            return JsonResponse({'error': 'Invalid subject code'}, status=400)

        # Fetch the student based on the name (you could use a roll number instead if necessary)
        student = User.objects.filter(username=student_name).first()  # Assuming 'username' is used for student identification

        if not student:
            return JsonResponse({'error': 'Student not found'}, status=404)

        # Capture the student's IP address
        ip_address = request.META.get('REMOTE_ADDR')

        # Create an attendance record with the status "P" (Present)
        attendance = Attendance.objects.create(
            student=student,
            subject=subject,
            date=timestamp,  # Use the timestamp from the QR code for attendance marking
            status="P",  # Mark as "Present"
            ip_address=ip_address  # Record the student's IP address
        )

        return JsonResponse({'message': 'Attendance marked successfully'}, status=200)

    return render(request, 'mark_attendance.html')  # Render the attendance page for GET requests



def generate_qr(request):
    qr_code_url = None  # Default to None if no QR code is generated

    if request.method == 'POST':
        subject_code = request.POST.get('subject_id')  # Get subject ID (e.g., 'ai101')

        # Validate if subject exists using subject_code
        try:
            subject = Subject.objects.get(code=subject_code)  # Query by subject code
        except Subject.DoesNotExist:
            return HttpResponse("Invalid Subject Code.", status=400)

        # Generate the timestamp for the attendance record (optional)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Create the URL to be embedded in the QR code (including subject_id)
        qr_data = f"http://127.0.0.1:8000/login/?subject_id={subject.code}"

        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert the QR code image to base64 and prepare it for display
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Convert the image buffer to base64
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        qr_code_url = f"data:image/png;base64,{qr_code_base64}"  # Set the base64-encoded image data

    return render(request, 'generate_qr_code.html', {'qr_code': qr_code_url})


@login_required
def student_dashboard(request):
    # Fetch the student's information from the session or database
    student = Student.objects.get(user=request.user)  # Assuming a User model is linked to Student

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

@login_required
def submit_attendance(request):
    if request.method == 'POST':
        # Submit attendance form
        student_name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')
        subject = request.POST.get('subject')

        # Logic to save the attendance, for example:
        student = Student.objects.get(name=student_name, roll_number=roll_number)
        # Create attendance record (assuming an Attendance model exists)
        # Attendance.objects.create(student=student, subject=subject)

        return redirect('student_dashboard')  # Redirect back to the student dashboard or another page

    return render(request, 'attendance_form.html')  # If not a POST request, show the form


@login_required
def my_view(request):
    # Your view logic
    return render(request, 'my_template.html')


def display_student_profiles(request):
    profiles = StudentProfile.objects.all()
    return render(request, 'attendance/display_profiles.html', {'profiles': profiles})


def create_student_with_password(h_t_no, student_name):
    # Use the Hall Ticket Number as the password and hash it
    hashed_password = make_password(h_t_no)  # The hall ticket number is hashed as the password

    # Create and save the student object
    student = Student(h_t_no=h_t_no, name=student_name, password=hashed_password)
    student.save()

    return student


def create_student_user(student):
    # Create a new user, using the student's hall ticket number as the username and generating a password
    user = User.objects.create_user(username=student.h_t_no, password=student.generate_password())
    
    # Use the student's full name as the first name and leave the last name as an empty string
    user.first_name = student.name  # Set full name as the first name
    user.last_name = ''  # Leave last name empty
    user.save()
    
    return user

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


def attendance_details(request):
    # Get the logged-in student's attendance details
    student = request.user  # Assuming the user is a logged-in student

    # Fetch attendance for the logged-in student (you can customize this query)
    attendance_records = Attendance.objects.filter(student=student)

    return render(request, 'attendance_details.html', {
        'attendance_records': attendance_records
    })

def verify_student_password(h_t_no, password):
    try:
        # Fetch the student from the database by Hall Ticket Number (h_t_no)
        student = Student.objects.get(h_t_no=h_t_no)

        # Check if the entered password matches the stored hashed password
        if check_password(password, student.password):
            print("Password is correct!")  # Success
        else:
            print("Incorrect password.")  # Failure
    except Student.DoesNotExist:
        print("Student not found.")  # Error: Student does not exist



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
    

def create_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        h_t_no = request.POST.get('h_t_no')
        name = request.POST.get('name')
        section = request.POST.get('section')
        branch = request.POST.get('branch')

        # Create the User object
        user = User.objects.create_user(username=username, password=password)

        # Create the Student object
        student = Student.objects.create(
            user=user,
            h_t_no=h_t_no,
            name=name,
            section=section,
            branch=branch
        )
        return redirect('student_profile')  # Redirect to a profile page or wherever needed
    return render(request, 'create_student.html')



'''def student_login(request):
    if request.method == 'POST':
        # Get student data from the form
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            # Fetch the student using the name
            student = Student.objects.get(name=name)
            #print(student.password,password,student.password==password,check_password(password, student.password))

            # Check if the entered password matches the stored hashed password
            if check_password(password, student.password):
                # If password is correct, store session data and redirect to attendance form
                request.session['name'] = student.name
                return redirect('attendance_form')  # Redirect to the attendance form
            else:
                # If password doesn't match
                return render(request, 'student_login.html', {'error': 'Invalid password or student name.'})

        except Student.DoesNotExist:
            # If the student doesn't exist
            return render(request, 'student_login.html', {'error': 'Student not found.'})

    return render(request, 'student_login.html')'''


'''def student_login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(name=name, password=password)
            request.session['name'] = student.name
            # Check if subject_id exists in the URL and store it in session
            subject_id = request.GET.get('subject_id')
            if subject_id:
                request.session['subject_id'] = subject_id
            return redirect('attendance_form')  # Redirect to the attendance form after login
        except Student.DoesNotExist:
            return HttpResponse("Invalid credentials", status=400)

    return render(request, 'student_login.html')'''

'''
@csrf_exempt
def submit_attendance(request):
    if request.method == 'POST':
        # Get the data from the POST request
        student_name = request.POST.get('name')  # The student name
        subject_code = request.POST.get('subject')  # The subject code
        timestamp = request.POST.get('timestamp')  # The timestamp from the QR code

        # Fetch the subject using the subject code
        try:
            subject = Subject.objects.get(code=subject_code)
        except Subject.DoesNotExist:
            return JsonResponse({'error': 'Invalid subject code'}, status=400)

        # Fetch the student based on the name (you could use a roll number instead if necessary)
        student = User.objects.filter(username=student_name).first()  # Assuming 'username' is used for student identification

        if not student:
            return JsonResponse({'error': 'Student not found'}, status=404)

        # Capture the student's IP address
        ip_address = request.META.get('REMOTE_ADDR')

        # Create an attendance record with the status "P" (Present)
        attendance = Attendance.objects.create(
            student=student,
            subject=subject,
            date=timestamp,  # Use the timestamp from the QR code for attendance marking
            status="P",  # Mark as "Present"
            ip_address=ip_address  # Record the student's IP address
        )

        return JsonResponse({'message': 'Attendance marked successfully'}, status=200)

    return render(request, 'mark_attendance.html')  # Render the attendance page for GET requests


'''

'''def attendance_form(request):
    # Check if the user is logged in by checking the session
    if 'name' not in request.session:
        print("Session not found, redirecting to login.")  # Debugging
        return redirect('student_login')  # If not logged in, redirect to student login page

    name = request.session['name']
    try:
        student = Student.objects.get(name=name)
        print(f"Student found: {student.name}")  # Debugging: Print student name
    except Student.DoesNotExist:
        print("Student not found in session.")  # Debugging: No student found
        return redirect('student_login')

    # Handle the form submission if the student updates their details
    if request.method == 'POST':
        student.email = request.POST.get('email')
        student.phone_number = request.POST.get('phone_number')  # example additional detail
        student.save()
        print(f"Student details updated: {student.email}, {student.phone_number}")  # Debugging
        return redirect('attendance_form')  # Redirect back after saving the details

    return render(request, 'attendance_form.html', {'student': student})'''
'''#@login_required
def attendance_form(request):
    """
    This view handles the attendance form submission for a logged-in student.
    It checks if the student is logged in and allows them to update their details.
    """
    # The user is guaranteed to be logged in because of @login_required
    user = request.user  # The logged-in user, Django's User model
    
    try:
        # Get the student object associated with the logged-in user
        student = Student.objects.get(user=user)  # Assuming Student is related to the User model
        print(f"Student found: {student.name}")  # Debugging: Print student name
    except Student.DoesNotExist:
        # If no student is found, redirect to the login page
        print("Student not found in session.")  # Debugging: No student found
        return redirect('student_login')
    
    # If the form is submitted, update the student's details
    if request.method == 'POST':
        student.email = request.POST.get('email', student.email)  # If email is provided, update
        student.phone_number = request.POST.get('phone_number', student.phone_number)  # Update phone number if provided
        student.save()
        print(f"Student details updated: {student.email}, {student.phone_number}")  # Debugging
        return redirect('attendance_form')  # Redirect back to attendance form after saving

    # Render the attendance form template with the student's data
    return render(request, 'attendance/attendance_form.html', {'student': student})'''


'''
@login_required  # Ensure only logged-in users can access the form
def attendance_form(request):
    # Fetch the logged-in student's details
    student = request.user  # Assuming the user is a Student and using the built-in User model
    
    if request.method == 'POST':
        # When the form is submitted, process the data
        subject_code = request.POST.get('subject_code')  # Get the subject code from the form
        timestamp = timezone.now()  # Use the current timestamp for the attendance record
        
        try:
            subject = Subject.objects.get(code=subject_code)  # Fetch the subject by code
        except Subject.DoesNotExist:
            # Handle the case where the subject code is invalid
            return render(request, 'attendance_form.html', {'error': 'Invalid subject code.'})
        
        # Record the attendance (mark as present)
        attendance = Attendance.objects.create(
            student=student,
            subject=subject,
            date=timestamp,  # Set the current time as the attendance time
            status='P'  # Mark as Present (you can change this logic as needed)
        )

        # Redirect to a confirmation page or student dashboard after submission
        return redirect('attendance_success')  # Replace with the actual URL name for the success page
    
    # If it's a GET request, just show the form
    subjects = Subject.objects.all()  # Get all available subjects for the student
    return render(request, 'attendance/attendance_form.html', {'student': student, 'subjects': subjects})
'''