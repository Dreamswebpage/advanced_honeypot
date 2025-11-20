# 🛡️ Advanced Honeypot System (Flask-based)

This is an **Advanced Web Honeypot System** built using **Python Flask**, designed to trap attackers, log their activities, and monitor suspicious behavior without exposing the real system.

It provides:

- A **fake admin login panel** to attract attackers  
- A **fake admin dashboard**  
- Hidden **internal monitoring panel** for the real admin  
- Logging of **IP address, user-agents, HTTP requests, and credentials**  
- Full analysis dashboard of captured attempts  

---

## 📁 Project Structure

advanced_honeypot/
│
├─ app.py
├─ config.py
├─ db.py
├─ logger.py
├─ requirements.txt
│
├─ templates/
│ ├─ base.html
│ ├─ login.html
│ ├─ fake_admin.html
│ ├─ admin_login.html
│ ├─ logs.html
│ └─ 404.html
│
└─ static/
├─ css/
│ └─ style.css
└─ js/
└─ main.js


---

## 🚀 Features

### 🔹 Fake Login Page  
Attackers think this is a real login panel and try brute force attacks.

### 🔹 Fake Admin Dashboard  
Shows dummy statistics to mislead attackers.

### 🔹 Real Hidden Monitoring Panel  
Admin can view:

- Logged requests  
- Captured usernames  
- Captured passwords  
- Timestamps  
- IP Addresses  
- User-Agent  

### 🔹 Full Request Logging  
Every request is captured using `before_request` hook.

### 🔹 Credentials Logging  
Every login attempt logs attacker credentials.

---

## 🧠 Technologies Used

- **Python 3.x**
- **Flask**
- **SQLite**
- **HTML / CSS / JS**
- **Gunicorn (for deployment)**

---

## ⚙️ Installation (Local Setup)

### 1️⃣ Clone the repository


### 2️⃣ Create virtual environment


### 3️⃣ Activate environment  
**Windows**



**Linux / Mac**


### 4️⃣ Install dependencies


### 5️⃣ Run the honeypot



### 6️⃣ Open in browser


http://localhost:8080/



---

## 🌐 Hosting on Render (Free Deployment)

### 1️⃣ Upload your files to GitHub  
Make sure ZIP upload is not used.  
Upload extracted files and folders.

### 2️⃣ Create account on Render  
https://render.com

### 3️⃣ Create a **New Web Service**

Choose:

- Build Command:


- Start Command:


### 4️⃣ Add this code in app.py for Render
```python
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

https://your-honeypot.onrender.com
