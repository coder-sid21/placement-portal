import sqlite3
import os
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"

    # make sure instance folder exists
    os.makedirs("instance", exist_ok=True)
    app.config["DATABASE"] = os.path.join("instance", "database.db")

    # -------------------------
    # Database connection
    # -------------------------
    def get_db():
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        return conn

    # -------------------------
    # Login required decorator
    # -------------------------
    def login_required(role=None):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                if "user_id" not in session:
                    return redirect("/login")

                if role and session.get("role") != role:
                    return "Unauthorized", 403

                return f(*args, **kwargs)
            return wrapper
        return decorator

    # -------------------------
    # Home
    # -------------------------
    @app.route("/")
    def home():
        return "Placement Portal Running 🚀"

    # -------------------------
    # Create Admin (one time)
    # -------------------------
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

    # -------------------------
    # Login
    # -------------------------
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            db = get_db()
            user = db.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            ).fetchone()

            if user and check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["role"] = user["role"]

                if user["role"] == "admin":
                    return redirect("/admin-dashboard")
                elif user["role"] == "company":
                    return redirect("/company-dashboard")
                else:
                    return redirect("/student-dashboard")

            return "Invalid credentials"

        return render_template("auth/login.html")

    # -------------------------
    # Logout
    # -------------------------
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/login")

    # -------------------------
    # Student Registration
    # -------------------------
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

    # -------------------------
    # Dashboards
    # -------------------------
    @app.route("/admin-dashboard")
    @login_required(role="admin")
    def admin_dashboard():
        return "Admin Dashboard"

    @app.route("/company-dashboard")
    @login_required(role="company")
    def company_dashboard():
        return "Company Dashboard"

    @app.route("/student-dashboard")
    @login_required(role="student")
    def student_dashboard():
        return "Student Dashboard"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)