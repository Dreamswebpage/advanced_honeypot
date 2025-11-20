# app.py

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, abort
)
from config import SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD, HIDDEN_ADMIN_PATH
from db import init_db, fetch_latest_requests, fetch_latest_credentials
from logger import capture_request, capture_credentials
import time

app = Flask(__name__)
app.secret_key = SECRET_KEY

# App start par DB init
init_db()

@app.before_request
def before_any_request():
    # Har request ko log karo
    capture_request()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# ---------- Fake public site (honeypot) ----------

@app.route("/", methods=["GET"])
def index():
    # Fake login page
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # Attacker ke credentials store karo
    capture_credentials(username, password)

    # Thoda delay daal do (real jaisa feel)
    time.sleep(2)

    # Hamesha invalid dikhana hai (taaki attacker bar-bar try kare)
    flash("Invalid username or password. Please try again.", "error")
    return redirect(url_for("index"))

@app.route("/dashboard")
def fake_dashboard():
    # Agar koi user direct /dashboard hit kare to bhi fake admin panel dikhao
    fake_stats = {
        "total_users": 5230,
        "monthly_revenue": "$12,340",
        "pending_tickets": 87
    }
    return render_template("fake_admin.html", stats=fake_stats)

# ---------- Hidden real admin panel (tumhare liye) ----------

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
        abort(404)  # direct 404, taki attacker ko panel ka pata na lage

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

if __name__ == "__main__":
    # Development mode
    app.run(host="0.0.0.0", port=8080, debug=False)
