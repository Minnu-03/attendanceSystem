from django.core.management.base import BaseCommand
from attendance.models import Student
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Sets the password for a student'

    def handle(self, *args, **kwargs):
        # Fetch Dhruv's record
        try:
            student = Student.objects.get(name='Dhruv')

            # Set and hash the password
            student.password = make_password('dhruv1234')  # Securely hash the password

            # Save the updated student record
            student.save()

            self.stdout.write(self.style.SUCCESS('Password for Dhruv has been updated successfully.'))
        except Student.DoesNotExist:
            self.stdout.write(self.style.ERROR('Student with the name Dhruv does not exist.'))
