import sqlite3
import os
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"

    os.makedirs("instance", exist_ok=True)
    app.config["DATABASE"] = os.path.join("instance", "database.db")

    # ---------------------------
    # Database
    # ---------------------------
    def get_db():
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        return conn

    # ---------------------------
    # Login Required Decorator
    # ---------------------------
    def login_required(role=None):

        def decorator(f):

            @wraps(f)
            def wrapper(*args, **kwargs):

                if "user_id" not in session:
                    return redirect("/login")

                if role and session.get("role") != role:
                    return render_template("errors/403.html")

                return f(*args, **kwargs)

            return wrapper

        return decorator

    # ---------------------------
    # Home
    # ---------------------------
    @app.route("/")
    def home():
        return render_template("home.html")

    # ---------------------------
    # Create Admin (run once)
    # ---------------------------
    @app.route("/create-admin")
    def create_admin():
        db = get_db()
        password = generate_password_hash("admin123")

        try:
            db.execute(
                "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
                ("admin@portal.com", password, "admin")
            )
            db.commit()
            return "Admin created successfully!"
        except:
            return "Admin already exists."

    # ---------------------------
    # Login
    # ---------------------------
    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":

            email = request.form["email"]
            password = request.form["password"]

            db = get_db()

            user = db.execute(
                "SELECT * FROM users WHERE email=?",
                (email,)
            ).fetchone()

            if user and check_password_hash(user["password_hash"], password):

                session["user_id"] = user["id"]
                session["role"] = user["role"]

                if user["role"] == "admin":
                    return redirect("/admin-dashboard")

                elif user["role"] == "company":

                    company = db.execute(
                        "SELECT * FROM companies WHERE user_id=?",
                        (user["id"],)
                    ).fetchone()

                    if company["approval_status"] != "Approved":

                        flash("Your company account is not approved by admin yet.", "warning")

                        return redirect("/login")

                    return redirect("/company-dashboard")
                else:
                    return redirect("/student-dashboard")

            else:
                flash("Invalid email or password", "danger")
                
                

        return render_template("auth/login.html")

    # ---------------------------
    # Logout
    # ---------------------------
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")
    



    # ---------------------------
    # Student Registration
    # ---------------------------
    @app.route("/register-student", methods=["GET", "POST"])
    def register_student():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            full_name = request.form["full_name"]
            branch = request.form["branch"]

            db = get_db()
            hashed_password = generate_password_hash(password)

            try:
                cursor = db.execute(
                    "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
                    (email, hashed_password, "student")
                )
                user_id = cursor.lastrowid

                db.execute(
                    "INSERT INTO students (user_id, full_name, branch) VALUES (?, ?, ?)",
                    (user_id, full_name, branch)
                )

                db.commit()
                return redirect("/login")

            except:
                return "Email already exists"

        return render_template("auth/register_student.html")

    # ---------------------------
    # Company Registration
    # ---------------------------
    @app.route("/register-company", methods=["GET", "POST"])
    def register_company():

        if request.method == "POST":

            email = request.form["email"]
            password = request.form["password"]
            company_name = request.form["company_name"]
            website = request.form["website"]

            db = get_db()

            hashed_password = generate_password_hash(password)

            try:

                cursor = db.execute(
                    "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
                    (email, hashed_password, "company")
                )

                user_id = cursor.lastrowid

                db.execute(
                    """INSERT INTO companies
                    (user_id, company_name, website, approval_status)
                    VALUES (?, ?, ?, ?)""",
                    (user_id, company_name, website, "Pending")
                )

                db.commit()

                flash("Company registered successfully. Wait for admin approval.", "success")

                return redirect("/login")

            except:

                flash("Email already exists", "danger")

        return render_template("auth/register_company.html")

    # ---------------------------
    # Dashboards
    # ---------------------------
    @app.route("/admin-dashboard")
    @login_required(role="admin")
    def admin_dashboard():
        db = get_db()

        students = db.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        companies = db.execute(
            "SELECT COUNT(*) FROM companies"
        ).fetchone()[0]

        drives = db.execute(
            "SELECT COUNT(*) FROM placement_drives"
        ).fetchone()[0]

        applications = db.execute(
            "SELECT COUNT(*) FROM applications"
        ).fetchone()[0]

        return render_template(
            "admin/dashboard.html",
            students=students,
            companies=companies,
            drives=drives,
            applications=applications
        )

    @app.route("/company-dashboard")
    @login_required(role="company")
    def company_dashboard():

        db = get_db()

        company = db.execute(
            "SELECT * FROM companies WHERE user_id=?",
            (session["user_id"],)
        ).fetchone()

        drives = db.execute(
            "SELECT * FROM placement_drives WHERE company_id=?",
            (company["id"],)
        ).fetchall()

        return render_template(
            "company/dashboard.html",
            company=company,
            drives=drives
        )

    @app.route("/student-dashboard")
    @login_required(role="student")
    def student_dashboard():
        return render_template("student/dashboard.html")

    # ---------------------------
    # Admin View Companies
    # ---------------------------
    @app.route("/admin/companies")
    @login_required(role="admin")
    def view_companies():
        db = get_db()
        companies = db.execute(
            "SELECT * FROM companies WHERE approval_status = 'Pending'"
        ).fetchall()

        return render_template("admin/view_companies.html", companies=companies)

    # ---------------------------
    # Approve Company
    # ---------------------------
    @app.route("/admin/approve-company/<int:company_id>")
    @login_required(role="admin")
    def approve_company(company_id):
        db = get_db()
        db.execute(
            "UPDATE companies SET approval_status = 'Approved' WHERE id = ?",
            (company_id,)
        )
        db.commit()

        return redirect("/admin/companies")
    
    @app.route("/company/create-drive", methods=["GET", "POST"])
    @login_required(role="company")
    def create_drive():
        if request.method == "POST":
            job_title = request.form["job_title"]
            job_description = request.form["job_description"]
            eligibility = request.form["eligibility"]
            package = request.form["package"]
            location = request.form["location"]
            deadline = request.form["deadline"]

            db = get_db()

            # get company id using logged-in user
            company = db.execute(
                "SELECT * FROM companies WHERE user_id = ?",
                (session["user_id"],)
            ).fetchone()

            db.execute(
                """INSERT INTO placement_drives 
                (company_id, job_title, job_description, eligibility, package, location, application_deadline, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (company["id"], job_title, job_description, eligibility, package, location, deadline, "Pending")
            )

            db.commit()
            return redirect("/company-dashboard")
        return render_template("company/create_drive.html")
    # ---------------------------
    # Admin View Drives
    # ---------------------------
    @app.route("/admin/drives")
    @login_required(role="admin")
    def view_drives():
        db = get_db()

        drives = db.execute(
            """
            SELECT placement_drives.*, companies.company_name
            FROM placement_drives
            JOIN companies ON placement_drives.company_id = companies.id
            WHERE placement_drives.status = 'Pending'
            """
        ).fetchall()

        return render_template("admin/view_drives.html", drives=drives)

    # ---------------------------
    # Approve Drive
    # ---------------------------
    @app.route("/admin/approve-drive/<int:drive_id>")
    @login_required(role="admin")
    def approve_drive(drive_id):
        db = get_db()

        db.execute(
            "UPDATE placement_drives SET status = 'Approved' WHERE id = ?",
            (drive_id,)
        )

        db.commit()

        return redirect("/admin/drives")
        return render_template("admin/view_drives.html", drives=drives)
    @app.route("/student/drives")
    @login_required(role="student")
    def student_drives():
        db = get_db()

        drives = db.execute(
            """
            SELECT placement_drives.*, companies.company_name
            FROM placement_drives
            JOIN companies ON placement_drives.company_id = companies.id
            WHERE placement_drives.status = 'Approved'
            """
        ).fetchall()

        return render_template("student/view_drives.html", drives=drives)
    
    @app.route("/student/apply/<int:drive_id>")
    @login_required(role="student")
    def apply_drive(drive_id):
        db = get_db()

        student = db.execute(
            "SELECT * FROM students WHERE user_id = ?",
            (session["user_id"],)
        ).fetchone()

        # Check if already applied
        existing = db.execute(
            "SELECT * FROM applications WHERE student_id = ? AND drive_id = ?",
            (student["id"], drive_id)
        ).fetchone()

        if existing:
            return render_template("student/already_applied.html")

        db.execute(
            "INSERT INTO applications (student_id, drive_id, status) VALUES (?, ?, ?)",
            (student["id"], drive_id, "Applied")
        )

        db.commit()

        return render_template("student/apply_success.html")
    
    @app.route("/student/applications")
    @login_required(role="student")
    def student_applications():
        db = get_db()

        student = db.execute(
            "SELECT * FROM students WHERE user_id = ?",
            (session["user_id"],)
        ).fetchone()

        applications = db.execute(
            """
            SELECT applications.*, placement_drives.job_title,
                companies.company_name
            FROM applications
            JOIN placement_drives
                ON applications.drive_id = placement_drives.id
            JOIN companies
                ON placement_drives.company_id = companies.id
            WHERE applications.student_id = ?
            """,
            (student["id"],)
        ).fetchall()

        return render_template("student/applications.html", applications=applications)
    @app.route("/student/profile", methods=["GET", "POST"])
    @login_required(role="student")
    def student_profile():

        db = get_db()

        student = db.execute(
            "SELECT * FROM students WHERE user_id=?",
            (session["user_id"],)
        ).fetchone()

        if request.method == "POST":

            cgpa = request.form["cgpa"]

            db.execute(
                "UPDATE students SET cgpa=? WHERE id=?",
                (cgpa, student["id"])
            )

            db.commit()

            return redirect("/student/profile")

        return render_template("student/profile.html", student=student)
    
    @app.route("/reset-admin-password")
    def reset_admin_password():

        db = get_db()

        new_password = generate_password_hash("admin123")

        db.execute(
            "UPDATE users SET password_hash=? WHERE email=?",
            (new_password, "admin@portal.com")
        )

        db.commit()

        return "Admin password reset to admin123"
    return app
    
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5001)