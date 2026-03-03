import sqlite3
from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # Ensure instance folder exists
    os.makedirs("instance", exist_ok=True)

    app.config['DATABASE'] = os.path.join("instance", "database.db")

    def get_db():
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        return conn

    def init_db():
        db = get_db()
        with open("schema.sql") as f:
            db.executescript(f.read())
        db.close()

    @app.route("/")
    def home():
        return "Placement Portal Running 🚀"

    @app.route("/init-db")
    def initialize_database():
        init_db()
        return "Database Initialized Successfully ✅"

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)