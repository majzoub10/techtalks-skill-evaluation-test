from flask import Flask, request, session, render_template, redirect, url_for
from werkzeug.security import check_password_hash
from connection import get_connection

app = Flask(__name__)
app.secret_key = "YOUR_SECRET_KEY"

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return render_template("login.html", error="Email and password required")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT user_id, password FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user or not check_password_hash(user["password"], password):
            return render_template("login.html", error="Invalid credentials")

        session["user_id"] = user["user_id"]

        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")
