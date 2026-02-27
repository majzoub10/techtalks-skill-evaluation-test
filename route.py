from flask import Flask, jsonify, render_template
from connection import get_connection


app = Flask(__name__)


@app.route("/admin/dashboard")
def dashboard_page():
    return render_template("dashboard.html")


@app.route("/api/admin/dashboard", methods=["GET"])
def dashboard_data():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total_users FROM users")
        total_users = cursor.fetchone()["total_users"]

        cursor.execute("SELECT COUNT(*) AS total_skills FROM skills")
        total_skills = cursor.fetchone()["total_skills"]

        cursor.execute("""
            SELECT s.name,
                   IFNULL(AVG(uss.score_percentage), 0) AS avg_score
            FROM skills s
            LEFT JOIN user_skill_scores uss
                   ON s.skill_id = uss.skill_id
            GROUP BY s.skill_id, s.name
            ORDER BY s.name ASC
        """)

        skill_data = cursor.fetchall()

        skill_names = []
        skill_avg_scores = []

        for row in skill_data:
            skill_names.append(row["name"])
            skill_avg_scores.append(float(row["avg_score"]))

        cursor.execute("""
            SELECT s.name, uss.score_percentage
            FROM user_skill_scores uss
            JOIN skills s
              ON uss.skill_id = s.skill_id
            ORDER BY uss.score_percentage DESC
            LIMIT 1
        """)

        highest_result = cursor.fetchone()

        if highest_result:
            highest_score = highest_result["score_percentage"]
            highest_skill_name = highest_result["name"]
        else:
            highest_score = 0
            highest_skill_name = "N/A"

        cursor.close()
        conn.close()

        return jsonify({
            "total_users": total_users,
            "total_skills": total_skills,
            "skill_names": skill_names,
            "skill_avg_scores": skill_avg_scores,
            "highest_score": highest_score,
            "highest_skill_name": highest_skill_name
        })

    except Exception as e:
        return jsonify({
            "error": "Server error",
            "details": str(e)
        }), 500


@app.route("/api/debug")
def debug():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT DATABASE() AS db_name")
    db = cursor.fetchone()

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT * FROM skills")
    skills = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        "connected_to": db,
        "tables": tables,
        "users": users,
        "skills": skills
    })


if __name__ == "__main__":
    app.run(debug=True)
