from flask import Flask, request, render_template_string, session

# FLAW 1: hard-coded, guessable secret key makes signed sessions easier to forge.
app = Flask(__name__)
app.secret_key = "ironpulse-secret"

@app.route("/")
def home():
    return """
    <h1>IronPulse Lab</h1>
    <p>Educational Flask application containing three intentional security flaws.</p>
    <form action="/lookup" method="get">
        <label>Search username:</label>
        <input name="username" value="alice">
        <button type="submit">Search</button>
    </form>
    <p><a href="/profile?user_id=1">View profile 1</a></p>
    """

if __name__ == "__main__":
    app.run()
