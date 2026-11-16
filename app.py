
from flask import Flask, request, render_template_string

app = Flask(__name__)

# FLAW 1: Hardcoded and weak secret key
app.secret_key = "ironpulse-secret"

# FLAW 2: Hardcoded administrator password
ADMIN_PASSWORD = "admin123"

# Temporary storage for fitness bookings
bookings = []

HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>IronPulse Fitness</title>
</head>
<body>
    <h1>IronPulse Fitness Booking System</h1>

    <h2>Book Your Fitness Session</h2>

    <form action="/book" method="POST">
        <label>Full Name:</label>
        <input type="text" name="name">
        <br><br>

        <label>Email:</label>
        <input type="text" name="email">
        <br><br>

        <label>Phone:</label>
        <input type="text" name="phone">
        <br><br>

        <label>Fitness Session:</label>
        <select name="session">
            <option>Personal Training</option>
            <option>Yoga</option>
            <option>Cardio</option>
            <option>Strength Training</option>
        </select>
        <br><br>

        <button type="submit">Book Now</button>
    </form>

    <p><a href="/admin">Administrator Login</a></p>
</body>
</html>
"""

# FLAW 3: No input validation on booking details
@app.route("/")
def home():
    return render_template_string(HOME_PAGE)


@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    session_type = request.form.get("session")

    # Intentionally accepts empty or invalid input
    bookings.append({
        "name": name,
        "email": email,
        "phone": phone,
        "session": session_type
    })

    return """
    <h2>Booking Submitted Successfully!</h2>
    <a href="/">Back to Home</a>
    """


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")

        if password == ADMIN_PASSWORD:
            return render_template_string(
                "<h2>Admin Panel</h2><pre>{{ data }}</pre>",
                data=bookings
            )

        return "<h3>Incorrect Password</h3>"

    return """
    <h2>Administrator Login</h2>
    <form method="POST">
        <input type="password" name="password"
               placeholder="Enter admin password">
        <button type="submit">Login</button>
    </form>
    """


if __name__ == "__main__":
    app.run(debug=True)
