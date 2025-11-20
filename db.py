# db.py

import sqlite3
from datetime import datetime
from config import DATABASE_PATH

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Requests table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            method TEXT,
            path TEXT,
            user_agent TEXT,
            referer TEXT
        )
    """)

    # Credentials table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            username TEXT,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

def log_request(ip, method, path, user_agent, referer):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO requests (timestamp, ip, method, path, user_agent, referer)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        ip,
        method,
        path,
        user_agent[:300],
        (referer or "")[:300]
    ))
    conn.commit()
    conn.close()

def log_credentials(ip, username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO credentials (timestamp, ip, username, password)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        ip,
        username,
        password
    ))
    conn.commit()
    conn.close()

def fetch_latest_requests(limit=50):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_latest_credentials(limit=50):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM credentials ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows
