import sqlite3
import os

db_path = os.path.join("backend", "study_planner.db") # Let's find the correct path
if not os.path.exists(db_path):
    # Try alternate path
    db_path = os.path.join("database.db") 

print(f"Checking DB at: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(tasks);")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
