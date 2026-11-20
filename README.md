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


## Automated Security Scanning and CI Pipeline

This project uses GitHub Actions to automate security testing.

### Security Tools

- **Bandit:** Scans Python source code for common security issues.
- **Gitleaks:** Scans the repository for exposed secrets and credentials.

### CI Workflow

The GitHub Actions workflow is located at:

`.github/workflows/ci.yml`

The pipeline runs automatically on:
- Push events to the main branch.
- Pull requests targeting the main branch.

### Workflow Steps

1. Checkout the repository.
2. Set up Python 3.11.
3. Install Bandit.
4. Run Bandit security scanning.
5. Run Gitleaks secret scanning.

Both security scanning steps completed successfully in the latest workflow run.

## Understanding CI Results

GitHub Actions runs the security and CI workflow when code is pushed to the `main` branch or when a pull request targets `main`.
### How to Check CI Results

To view CI results, open the GitHub repository and click the **Actions** tab. Select the latest workflow run to view its status and logs.

### Understanding Bandit Results

A green check means the Bandit scan completed successfully. A red cross means the Bandit step failed. This may happen when security findings meet the configured severity threshold or when a scanning error occurs. Check the Bandit logs for details.

### Understanding Gitleaks Results

A green check means Gitleaks completed without detecting secrets that caused the scan to fail. A red cross may indicate a detected secret or a scanning error.

When reviewing a Gitleaks finding, check:
- **RuleID:** Which detection rule matched the secret.
- **File:** Where the finding was detected.
- **Line:** The line containing the finding.
- **Commit:** The commit that introduced the finding.
- **Leaks found:** The total number of detected secrets.

### Green Run (Success)

A green check mark means the workflow completed successfully. The configured Bandit and Gitleaks scans did not report findings that caused the workflow to fail.

### Red Run (Failure)

A red cross means one or more workflow steps failed. Open the failed workflow run, select the failed job, and review the logs to identify the cause. A failure may indicate a security finding, a configuration problem, or another workflow error.

### Reading Gitleaks Results

When Gitleaks detects a possible secret, review these fields in the workflow logs:

- **Finding:** The detected secret value. GitHub may redact it.
- **RuleID:** The rule that identified the possible secret.
- **File:** The file containing the finding.
- **Line:** The line number where the finding was detected.
- **Commit:** The commit containing the finding.
- **Leaks found:** The number of detected findings.

A Gitleaks finding causes the security scan to fail intentionally. Review the finding, remove the exposed secret, and use a secure method such as GitHub Actions secrets for sensitive values. Do not commit real credentials to the repository.

### Limitations of Default Gitleaks Detection

### Gitleaks Detection Limitations

Gitleaks default rules detect secrets that match known token formats and patterns, not every arbitrary hardcoded string. Therefore, `ADMIN_PASSWORD = "admin123"` and `app.secret_key = "ironpulse-secret"` in `app.py` are not detected. The next steps are to add custom detection rules in `.gitleaks.toml` or move sensitive values into environment variables.