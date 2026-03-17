import sqlite3

conn = sqlite3.connect("classroom_ai.db")
cur = conn.cursor()

# Create students table
cur.execute("""
CREATE TABLE IF NOT EXISTS students(
roll INTEGER PRIMARY KEY,
name TEXT,
age INTEGER,
final_attention REAL
)
""")

# Create sessions table
cur.execute("""
CREATE TABLE IF NOT EXISTS sessions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
roll INTEGER,
name TEXT,
attention REAL,
session_time TEXT
)
""")

# Insert demo students
cur.execute("INSERT INTO students VALUES (1001,'Arnab Das',8,45.01)")
cur.execute("INSERT INTO students VALUES (1002,'Sarah Khan',9,78.34)")
cur.execute("INSERT INTO students VALUES (1003,'Kevin Thomas',8,68.21)")

conn.commit()
conn.close()

print("Database and tables created successfully")