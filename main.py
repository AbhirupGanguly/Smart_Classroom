import random
import time
import sqlite3
import datetime
from colorama import Fore, init

init(autoreset=True)

# -----------------------------
# CONNECT TO SQLITE DATABASE
# -----------------------------
conn = sqlite3.connect("classroom_ai.db")
cursor = conn.cursor()

# -----------------------------
# CREATE TABLES IF NOT EXISTS
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    final_attention REAL
)
""")

# NEW: SESSION HISTORY TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll INTEGER,
    name TEXT,
    attention REAL,
    session_time TEXT
)
""")

# -----------------------------
# INSERT STUDENTS (IF NOT EXISTS)
# -----------------------------
students_data = [
    (1001, "Arnab Das", 8, 0),
    (1009, "Priya Sharma", 7, 0),
    (1003, "Kevin Thomas", 4, 0),
    (1034, "Meera Nair", 9, 0),
    (1045, "Sarah Khan", 6, 0),
]

for s in students_data:
    cursor.execute("INSERT OR IGNORE INTO students VALUES (?, ?, ?, ?)", s)

conn.commit()

# -----------------------------
# FETCH STUDENTS FROM DB
# -----------------------------
cursor.execute("SELECT roll, name, age FROM students")
rows = cursor.fetchall()

STUDENTS = []
for r in rows:
    STUDENTS.append({
        "roll": r[0],
        "name": r[1],
        "age": r[2]
    })

attention_sum = {s["roll"]: 0 for s in STUDENTS}
attention_count = {s["roll"]: 0 for s in STUDENTS}

# -----------------------------
# FUNCTIONS
# -----------------------------
def get_bar(score):
    filled = int(score * 10)
    return "█" * filled + "░" * (10 - filled)

def get_state(score):
    if score > 0.75:
        return "ACTIVE"
    elif score > 0.45:
        return "FOCUSED"
    else:
        return "DISTRACTED"

def print_header():
    print(Fore.CYAN + "CORE AI CLASSROOM ANALYTICS ENGINE (SQLITE ENABLED)")
    print("="*90)

def print_frame(frame_id):

    print(f"\n{Fore.MAGENTA}[ FRAME {frame_id} ANALYSIS ]")
    print("-"*90)

    for _ in range(random.randint(5,8)):

        if random.random() < 0.8:
            s = random.choice(STUDENTS)
            score = round(random.uniform(0.2,0.95),3)
            state = get_state(score)

            print(
                f"> {s['name']:<13} | Roll:{s['roll']} | Age:{s['age']} | "
                f"{state:<10} | [{get_bar(score)}] {score}"
            )

            attention_sum[s['roll']] += score
            attention_count[s['roll']] += 1

    print("="*90)

# -----------------------------
# MAIN
# -----------------------------
def main():

    frames = [120,150,180,210,240,270]
    print_header()

    for f in frames:
        print_frame(f)
        time.sleep(0.6)

    print("\nSaving Final Attention Scores to SQL Database...\n")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for roll in attention_sum:

        if attention_count[roll] > 0:
            final_score = (attention_sum[roll] / attention_count[roll]) * 100
        else:
            final_score = 0

        final_score = round(final_score, 2)

        # UPDATE latest score
        cursor.execute(
            "UPDATE students SET final_attention = ? WHERE roll = ?",
            (final_score, roll)
        )

        # INSERT session history record
        cursor.execute(
            "INSERT INTO sessions (roll, name, attention, session_time) VALUES (?, ?, ?, ?)",
            (
                roll,
                next(s["name"] for s in STUDENTS if s["roll"] == roll),
                final_score,
                now
            )
        )

        print(f"Roll {roll} → {final_score}% saved.")

    conn.commit()
    conn.close()

    print("\nSQL DATABASE UPDATED SUCCESSFULLY ✅")

if __name__ == "__main__":
    main()