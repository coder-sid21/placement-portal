# Placement Portal

A web-based **Placement Management System** built using **Flask, SQLite, and Bootstrap**.

This portal simulates a **college placement system** where:

- Students can view and apply to placement drives
- Companies can register and create placement drives
- Admin manages approvals and monitors the system

The goal of the project is to provide a **centralized platform for managing campus placements efficiently**.

---

# Features

## Student

- Register and login
- View approved placement drives
- Apply to placement drives
- Track application status
- Manage personal profile

## Company

- Register company account
- Wait for admin approval
- Create placement drives
- View created drives and their status

## Admin

- Dashboard with platform statistics
- Approve company registrations
- Approve placement drives
- Monitor system activities

---

# Tech Stack

## Backend
- Python
- Flask

## Frontend
- HTML
- Bootstrap 5
- Jinja Templates

## Database
- SQLite

## Version Control
- Git
- GitHub

---

# Project Structure

```text
placement_portal/
│
├── app.py
├── schema.sql
├── README.md
│
├── instance/
│   └── database.db
│
├── templates/
│
│   ├── base.html
│
│   ├── auth/
│   │   ├── login.html
│   │   ├── register_student.html
│   │   └── register_company.html
│
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── view_companies.html
│   │   └── view_drives.html
│
│   ├── student/
│   │   ├── dashboard.html
│   │   ├── drives.html
│   │   ├── applications.html
│   │   └── profile.html
│
│   └── company/
│       ├── dashboard.html
│       └── create_drive.html
```

---

# Installation

## 1 Clone the repository

```
git clone https://github.com/your-username/placement-portal.git
cd placement-portal
```

## 2 Create a virtual environment

```
python -m venv venv
```

## 3 Activate the environment

### Mac / Linux

```
source venv/bin/activate
```

### Windows

```
venv\Scripts\activate
```

## 4 Install dependencies

```
pip install flask
```

## 5 Initialize the database

Open this once in your browser:

```
http://127.0.0.1:5000/init-db
```

## 6 Run the application

```
python app.py
```

Open the project:

```
http://127.0.0.1:5000
```

---

# Default Admin Credentials

```
Email: admin@portal.com
Password: admin123
```

Admin can approve companies and placement drives from the admin dashboard.

---

# Application Workflow

The portal follows a structured workflow involving **Admin, Company, and Student**.

```text
1. Company Registration
   Company registers on the portal.

2. Admin Approval
   Admin reviews and approves the company.

3. Company Login
   Once approved, the company can log in.

4. Create Placement Drive
   Company creates a job drive.

5. Drive Approval
   Admin reviews and approves the drive.

6. Student Access
   Approved drives become visible to students.

7. Student Application
   Students apply to drives.

8. Application Tracking
   Students track applications and companies review applicants.
```

## Workflow Diagram

```text
Company Register
        ↓
Admin Approves Company
        ↓
Company Creates Drive
        ↓
Admin Approves Drive
        ↓
Students View Drives
        ↓
Students Apply
        ↓
Applications Stored in System
```

---

# Screens Included

- Login Page
- Student Dashboard
- Company Dashboard
- Admin Dashboard
- Placement Drive Listings
- Application Tracking

---

# Future Improvements

Possible improvements for the system:

- Resume upload and download
- Email notifications
- Interview scheduling
- Advanced admin analytics
- Application status updates
- Role-based permission system
- Password reset through email verification

---

# Author

Siddhartha Singh

---

# License

This project is developed for **educational purposes** and can be freely modified or extended.
