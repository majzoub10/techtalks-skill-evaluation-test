
from flask import Flask, request, jsonify, session, redirect, render_template
from werkzeug.security import check_password_hash

from connection import get_connection

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY"





@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid request"}), 400
    

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400
    



    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, password_hash FROM users WHERE email = %s",
        (email,)
    )

    
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    session["user_id"] = user["id"]
    return jsonify({"message": "Login successful"}), 200


@app.route("/login-page")
def login_page():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
