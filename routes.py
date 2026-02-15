from flask import Flask, redirect, render_template, request, session
from connection import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

import os
from dotenv import load_dotenv
import uuid

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/debug-db")
def debug_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    return f"Tables found in database: {tables}"


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    email = request.form["email"]
    plain_password = request.form["password"]

    # --- THE PRO TIP STEP ---
    hashed_pw = generate_password_hash(plain_password)
    # ------------------------

    conn = get_connection()
    cursor = conn.cursor()

    # Store the HASHED password, not the plain one
    cursor.execute("""
        INSERT INTO users (username, email, password)
        VALUES (%s, %s, %s)
    """, (username, email, hashed_pw))

    conn.commit()
    # ... rest of your code


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password_input = request.form["password"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT user_id, password FROM users WHERE email = %s",
        (email,)
    )
    user = cursor.fetchone()

    if user and check_password_hash(user["password"], password_input):
        # Success!
        session["user_id"] = user["user_id"]
        return redirect("/edit-profile")
    else:
        return "Invalid email or password"


@app.route("/test-login")
def test_login():
    session["user_id"] = 1   # ← Put the user_id from database
    return "Test user logged in!"


@app.route("/login-test")
def login_test():
    session["user_id"] = 1
    return redirect("/edit-profile")


@app.route("/edit-profile", methods=["GET"])
def edit_profile():

    if "user_id" not in session:
        return "Not logged in"

    user_id = session["user_id"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT username, age, date_of_birth, bio, profile_picture
        FROM users
        WHERE user_id = %s
    """, (user_id,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    success = request.args.get("success")

    return render_template("edit-profile.html", user=user, success=success)


@app.route("/update-profile", methods=["POST"])
def update_profile():

    if "user_id" not in session:
        return "Not logged in"

    user_id = session["user_id"]

    username = request.form["username"]
    age = request.form["age"]
    date_of_birth = request.form["date_of_birth"]
    bio = request.form["bio"]
    profile_picture = request.files["profile_picture"]

    conn = get_connection()
    cursor = conn.cursor()

    # Handle image upload
    if profile_picture and profile_picture.filename != "":
        file_ext = os.path.splitext(profile_picture.filename)[1]
        filename = str(uuid.uuid4()) + file_ext
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        profile_picture.save(image_path)

        cursor.execute("""
            UPDATE users
            SET username=%s, age=%s, date_of_birth=%s, bio=%s,
            profile_picture=%s
            WHERE user_id=%s
        """, (username, age, date_of_birth, bio, image_path, user_id))
    else:
        cursor.execute("""
            UPDATE users
            SET username=%s, age=%s, date_of_birth=%s, bio=%s
            WHERE user_id=%s
        """, (username, age, date_of_birth, bio, user_id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/edit-profile?success=1")


@app.route("/profile")
def profile():

    if "user_id" not in session:
        return "Not logged in"

    user_id = session["user_id"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit-profile.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
