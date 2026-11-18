# IronPulse Fitness – Flask Security Lab

## Project Overview

IronPulse Fitness is a simple Python Flask web application developed for an internship security-testing task.

The application allows users to submit fitness session bookings and provides an administrator login to view submitted bookings.

This project intentionally contains three security weaknesses for educational purposes. All testing is performed locally on the developer's own machine.

## Technologies Used

- Python
- Flask
- HTML
- Git and GitHub

## Application Features

- Fitness session booking form
- Customer name, email, and phone fields
- Fitness session selection
- Administrator login
- Display of submitted bookings

## Intentional Security Flaws

### 1. Hardcoded Administrator Password

**Location:** `app.py`

The administrator password is directly stored in the source code:

`ADMIN_PASSWORD = "admin123"`

**Security Risk:**

Anyone who can access the source code can discover the administrator password. Hardcoded credentials are difficult to manage securely and may be exposed if the code is shared.

**Manual Testing:**

- Open the Administrator Login page.
- Enter the test password `admin123`.
- Observe that the Admin Panel opens and displays booking information.

**Recommended Fix:**

Store credentials securely using environment variables or a secure authentication system. Store user passwords using an appropriate password-hashing algorithm.

### 2. Missing Input Validation

**Location:** `/book` route in `app.py`

The booking form accepts customer information without checking whether the submitted values are valid.

**Impact:**

This is primarily a data quality and reliability issue, not a direct security vulnerability. Users can submit empty names, invalid email addresses, and incorrect phone numbers, resulting in fake, incomplete, or unreliable booking records. Excessively long or repeated submissions may also consume application resources.

**Manual Testing:**

**Test 1:**
- Submit the booking form with all fields empty.
- Observe that the booking is accepted.

**Test 2:**
- Enter `not-an-email` as the email.
- Enter `abc123` as the phone number.
- Submit the booking form.
- Observe that the booking is accepted.

**Recommended Fix:**
- Validate all required fields on the server side.
- Check email and phone number formats.
- Set maximum input length limits.
- Implement rate limiting to reduce repeated submissions.

### 3. Weak Hardcoded Flask Secret Key

**Location:** `app.py`

The application uses a weak, predictable secret key:

`app.secret_key = "ironpulse-secret"`

**Security Risk:**

If Flask sessions are used with a predictable secret key, an attacker who knows the key may be able to forge session cookies.

The current application does not actively use session data, so this is a configuration weakness with a potential impact if sessions are introduced.

**Recommended Fix:**

Generate a strong random secret key and load it from a protected environment variable. Never commit production secrets to GitHub.

## Manual Security Testing Results

All tests were performed locally at:

`http://127.0.0.1:5000`

| Test | Actual Result |
|---|---|
| Submit empty booking form | Booking accepted |
| Submit invalid email and phone | Booking accepted |
| Login using hardcoded admin password | Admin Panel opened |
| Inspect Flask secret key | Weak hardcoded key identified |

## Testing Environment

- Operating System: Windows
- Code Editor: Visual Studio Code
- Programming Language: Python
- Framework: Flask
- Local Development Server: `127.0.0.1:5000`

## Security Disclaimer

This application is intentionally vulnerable and created only for educational security testing.

It must only be run in a controlled local development environment. Do not deploy it publicly, use real customer information, or use real passwords.

**Flaw 4: Flask Debug Mode Enabled**

**Location:** `app.py` — application startup.

**Security Impact:** 

Flask Debug Mode is disabled in the current application configuration.

Although enabling debug mode in production can expose sensitive information, this issue is not active in the current code.

Bandit did not report this as a vulnerability.

## Project Purpose

The purpose of this project is to understand common web application security weaknesses, identify them through manual testing, document their impact, and learn recommended security improvements.


## Bandit Security Scan Results

Bandit detected 2 potential security issues, both with Low severity:

- Hardcoded administrator password.
- Hardcoded Flask secret key.

No High severity issues were reported.

However, this does not mean the application is completely secure. Bandit performs static code analysis and cannot reliably identify every application-specific vulnerability, input validation issue, or runtime security problem.

Manual security testing and additional application-level testing are still necessary.
