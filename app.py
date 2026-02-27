
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

        # Check user table
        cursor.execute(
            "SELECT user_id, password FROM users WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["user_id"]
            session["role"] = "user"

            cursor.close()
            conn.close()
            return redirect(url_for("dashboard"))

        # Check admin table
        cursor.execute(
            "SELECT admin_id, password FROM admin WHERE email = %s",
            (email,)
        )
        admin = cursor.fetchone()

        cursor.close()
        conn.close()

        if admin and check_password_hash(admin["password"], password):
            session["admin_id"] = admin["admin_id"]
            session["role"] = "admin"
            return redirect(url_for("admindashboard"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")
