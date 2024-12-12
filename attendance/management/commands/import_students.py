from django.core.management.base import BaseCommand
import csv
from attendance.models import StudentProfile  # Replace 'your_app' with the actual app name

class Command(BaseCommand):
    help = 'Imports students from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str, help='Path to the CSV file containing student data.')

    def handle(self, *args, **options):
        try:
            with open(options['csv_filename'], mode='r', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Ensure the field names here match those in the CSV headers exactly
                    student, created = StudentProfile.objects.update_or_create(
                        hall_ticket_number=row['H.T.No'],  # CSV header for hall ticket number
                        defaults={
                            'section': row['Section'],  # CSV header for section
                            'branch': row['Branch'],  # CSV header for branch
                            'student_name': row['Student Name (as per SSC in CAPS)']  # CSV header for student name
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully created student: {student.student_name}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Updated existing student: {student.student_name}'))
        except UnicodeDecodeError:
            self.stdout.write(self.style.ERROR('Failed to decode CSV. Please check the file encoding.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
