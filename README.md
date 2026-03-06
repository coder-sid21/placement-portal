# Placement Portal

A web-based **Placement Management System** built using **Flask, SQLite, and Bootstrap**.  
The portal allows **students, companies, and administrators** to interact in a centralized system for managing placement drives and job applications.

This project simulates a real-world **college placement portal** where companies post opportunities, students apply, and the admin manages approvals.

---

## Features

### Student
- Register and login
- View approved placement drives
- Apply to drives
- Track application status
- Manage profile information

### Company
- Register company account
- Wait for admin approval
- Create placement drives
- View drives created and their approval status

### Admin
- Dashboard with system statistics
- Approve company registrations
- Approve placement drives
- Monitor the platform activity

---

## Tech Stack

**Backend**
- Python
- Flask

**Frontend**
- HTML
- Bootstrap 5
- Jinja Templates

**Database**
- SQLite

**Version Control**
- Git
- GitHub

---

## Project Structure
placement_portal
│
├── app.py
├── schema.sql
├── instance/
│ └── database.db
│
├── templates/
│ ├── base.html
│ │
│ ├── auth/
│ │ ├── login.html
│ │ ├── register_student.html
│ │ └── register_company.html
│ │
│ ├── admin/
│ │ ├── dashboard.html
│ │ ├── view_companies.html
│ │ └── view_drives.html
│ │
│ ├── student/
│ │ ├── dashboard.html
│ │ ├── drives.html
│ │ ├── applications.html
│ │ └── profile.html
│ │
│ └── company/
│ ├── dashboard.html
│ └── create_drive.html
│
└── README.md

---

## Installation

### 1 Clone the repository
git clone https://github.com/your-username/placement-portal.git

cd placement-portal


### 2 Create virtual environment


python -m venv venv


### 3 Activate environment

Mac / Linux


source venv/bin/activate


Windows


venv\Scripts\activate


### 4 Install dependencies


pip install flask


### 5 Initialize the database

Run this once in your browser:


http://127.0.0.1:5000/init-db


### 6 Run the application


python app.py


Then open:


http://127.0.0.1:5000


---

## Default Admin Credentials


Email: admin@portal.com

Password: admin123


Admin can approve companies and placement drives from the admin dashboard.

---

## Application Workflow


Company registers
↓
Admin approves company
↓
Company creates placement drive
↓
Admin approves drive
↓
Students view drives
↓
Students apply


---

## Screens Included

- Login Page
- Student Dashboard
- Company Dashboard
- Admin Dashboard
- Placement Drive Listings
- Application Tracking

---

## Future Improvements

Possible improvements that can be added:

- Resume upload and download
- Email notifications
- Interview scheduling
- Advanced admin analytics dashboard
- Application status updates
- Role-based permission system
- Password reset through email verification

---

## Author

Aparna Singh

---

## License

This project is created for **educational purposes** and can be freely modified or extended.
