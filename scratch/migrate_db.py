import sqlite3
import os

db_path = os.path.join("data", "database.db")
print(f"Connecting to: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check current columns
    cursor.execute("PRAGMA table_info(tasks);")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"Current columns: {columns}")
    
    if "description" not in columns:
        print("Adding description column...")
        cursor.execute("ALTER TABLE tasks ADD COLUMN description TEXT;")
        
    if "priority" not in columns:
        print("Adding priority column...")
        cursor.execute("ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Medium';")
        
    conn.commit()
    print("Database updated successfully!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
