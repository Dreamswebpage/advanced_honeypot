# app.py

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, abort
)
from config import SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD, HIDDEN_ADMIN_PATH
from db import init_db, fetch_latest_requests, fetch_latest_credentials
from logger import capture_request, capture_credentials
import time
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Database initialize on app start
init_db()

@app.before_request
def before_any_request():
    # Log every request
    capture_request()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# ---------- Fake Honeypot Public Interface ----------

@app.route("/", methods=["GET"])
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # Log attacker credentials
    capture_credentials(username, password)

    # Realistic delay
    time.sleep(2)

    # Always show error (honeypot behaviour)
    flash("Invalid username or password. Please try again.", "error")
    return redirect(url_for("index"))

@app.route("/dashboard")
def fake_dashboard():
    fake_stats = {
        "total_users": 5230,
        "monthly_revenue": "$12,340",
        "pending_tickets": 87
    }
    return render_template("fake_admin.html", stats=fake_stats)

# ---------- Hidden Admin Panel (For You Only) ----------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_authenticated"] = True
            flash("Logged in as admin.", "success")
            return redirect(HIDDEN_ADMIN_PATH)
        else:
            flash("Invalid admin credentials.", "error")
            return redirect(url_for("admin_login"))

    return render_template("admin_login.html")

def admin_required():
    if not session.get("admin_authenticated"):
        abort(404)

@app.route(HIDDEN_ADMIN_PATH, methods=["GET"])
def admin_panel():
    admin_required()
    reqs = fetch_latest_requests()
    creds = fetch_latest_credentials()
    return render_template("logs.html", requests=reqs, creds=creds)

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("Logged out.", "success")
    return redirect(url_for("index"))


# ---------- Production Server (Render Compatibility) ----------

if __name__ == "__main__":
    # Render provides PORT through environment variables
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
