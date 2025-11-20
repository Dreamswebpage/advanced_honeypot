# config.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SQLite database ka path
DATABASE_PATH = os.path.join(BASE_DIR, "honeypot.db")

# Flask secret key (session ke liye)
SECRET_KEY = "change_this_to_a_random_long_secret_key"

# Admin panel ka password (college demo ke liye simple rakho)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Admin@123"  # isko change kar lena

# Hidden admin panel ka URL path (thoda obfuscated)
HIDDEN_ADMIN_PATH = "/internal-monitor-panel"
