from flask import Flask, render_template, session
from connection import get_connection

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")


@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")

    if not user_id:

        return "Please log in to view your dashboard.", 401

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT
                s.name AS skill_name,
                uss.score_percentage,
                uss.last_updated
            FROM user_skill_scores uss
            JOIN skills s ON uss.skill_id = s.skill_id
            WHERE uss.user_id = %s
            ORDER BY uss.last_updated DESC
        """
        cursor.execute(query, (user_id,))
        skills = cursor.fetchall()

        for skill in skills:
            score = skill["score_percentage"]

            if score >= 85:
                skill["stars"] = 3
            elif score >= 75:
                skill["stars"] = 2
            elif score >= 60:
                skill["stars"] = 1
            else:
                skill["stars"] = 0

            if score >= 60:
                skill["status_text"] = "Verified"
                skill["css_class"] = "status-active"
            else:
                skill["status_text"] = "Not Verified"
                skill["css_class"] = "status-pending"

        return render_template("dash.html", skills=skills)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
