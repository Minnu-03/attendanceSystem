<h1>QR code based Attendance Management System</h1>

Traditional attendance systems can be time-consuming, prone to errors, and susceptible to proxy
attendances, where individuals falsely mark their presence instead of others. The "QR Code Attendance
System" is a fast, efficient, and user-friendly solution for tracking attendance through QR codes designed to address these challenges. Leveraging web-based technology automates and streamlines the attendance process, significantly reducing the likelihood of attendance manipulation. Built
with HTML, CSS, and Django, the system offers a seamless, real-time interface for marking presence. It operates within a local network environment. Ngrok is used to make the links publically accessible. Key features include Automatic IP Fetching, generation of QR code, and a Faculty Panel that enables educators to identify and eliminate proxy attendances. This ensures that only legitimate attendance is recorded, enhancing the accuracy of the system. Additionally, it provides a straightforward interface for ease of use, real-time tracking through QR code scanning, and quick access for managing attendance records.

How it works:

--> Faculty logs in using their credentials and enters the subject code to generate a QR code.

--> Students scan the QR code displayed by the faculty member.

--> Students are redirected to the login page, where they log in, fill out their attendance details, and click "Submit" to mark their attendance.

--> Submitted details are updated in the admin panel, where the teacher can view and update student information, attendance, and subjects.

--> Recorded details include: Name, Roll Number, Subject Code, IP Address, Date, and Timestamp.


![homePage](https://github.com/user-attachments/assets/95a84f8a-dec9-4b7c-812c-50ae48569d6f)


![qrGen](https://github.com/user-attachments/assets/9c9a404f-a1e5-47fe-8b65-4b09e0c8c84a)
