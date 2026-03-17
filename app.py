from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -----------------------------
# DATABASE CONNECTION FUNCTION
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect("classroom_ai.db")
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# GET ALL STUDENTS
# -----------------------------
@app.route("/api/students", methods=["GET"])
def get_students():

    conn = get_db_connection()
    students = conn.execute(
        "SELECT roll, name, age, final_attention FROM students"
    ).fetchall()
    conn.close()

    result = []

    for s in students:
        result.append({
            "roll": s["roll"],
            "name": s["name"],
            "age": s["age"],
            "final_attention": s["final_attention"]
        })

    return jsonify(result)

# -----------------------------
# GET SESSION HISTORY
# -----------------------------
@app.route("/api/sessions", methods=["GET"])
def get_sessions():

    conn = get_db_connection()
    sessions = conn.execute(
        "SELECT id, roll, name, attention, session_time FROM sessions ORDER BY id DESC"
    ).fetchall()
    conn.close()

    result = []

    for s in sessions:
        result.append({
            "id": s["id"],
            "roll": s["roll"],
            "name": s["name"],
            "attention": s["attention"],
            "session_time": s["session_time"]
        })

    return jsonify(result)

# -----------------------------
# GET SINGLE STUDENT HISTORY
# -----------------------------
@app.route("/api/student/<int:roll>", methods=["GET"])
def get_student(roll):

    conn = get_db_connection()
    sessions = conn.execute(
        "SELECT id, attention, session_time FROM sessions WHERE roll=?",
        (roll,)
    ).fetchall()
    conn.close()

    result = []

    for s in sessions:
        result.append({
            "id": s["id"],
            "attention": s["attention"],
            "session_time": s["session_time"]
        })

    return jsonify(result)

# -----------------------------
# ADD NEW STUDENT
# -----------------------------
@app.route("/api/add_student", methods=["POST"])
def add_student():

    data = request.json

    roll = data["roll"]
    name = data["name"]
    age = data["age"]

    conn = get_db_connection()

    conn.execute(
        "INSERT INTO students (roll, name, age, final_attention) VALUES (?, ?, ?, ?)",
        (roll, name, age, 0)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Student added successfully"})

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)