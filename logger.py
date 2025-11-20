# logger.py

from flask import request
from db import log_request, log_credentials

def capture_request():
    """Har request se info nikal kar DB me daalo."""
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    method = request.method
    path = request.path
    user_agent = request.headers.get("User-Agent", "")
    referer = request.headers.get("Referer", "")

    # Static files ko ignore karna ho to yahan condition laga sakte ho
    if not path.startswith("/static"):
        log_request(ip, method, path, user_agent, referer)

def capture_credentials(username, password):
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    log_credentials(ip, username, password)
