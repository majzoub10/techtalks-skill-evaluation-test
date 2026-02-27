from connection import get_connection

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT user_id, username, email FROM users")
users = cursor.fetchall()

print("Users found:", len(users))
for user in users:
    print(user)

cursor.close()
conn.close()
