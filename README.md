# IronPulse Lab

A small Flask application for learning to identify common web-application security flaws.
**This project is intentionally vulnerable. Run it only on your own computer for learning. Do not deploy it publicly.**

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Intentional flaws

### 1. Hard-coded Flask secret key
**Location:** `app.py`, near `app.secret_key`.

The application uses a predictable secret key stored directly in source code. Flask uses this key to sign session cookies. If an attacker knows the key, they may be able to create forged session data. In a real application, use a strong randomly generated secret stored in an environment variable and rotate it if exposed.

### 2. SQL injection
**Location:** `lookup()` route in `app.py`.

The `username` query parameter is concatenated directly into an SQL statement. Crafted input can change the meaning of the query. Use parameterized SQL statements (for example, `WHERE username = ?`) instead of string concatenation.

### 3. Insecure Direct Object Reference (IDOR)
**Location:** `profile()` route in `app.py`.

The route accepts any `user_id` from the URL and returns that profile without checking whether the requester is authorized to view it. A user can change `?user_id=1` to `?user_id=2` and access another profile. Enforce authentication and object-level authorization on every request.

## Git history

This project is organized into three commits:

1. `Create initial Flask application`
2. `Add three intentional security flaws for lab review`
3. `Document the three intentional security flaws`

## Safety note

The vulnerabilities are deliberately included as a training exercise. Do not use real personal data, credentials, or production databases with this application.
