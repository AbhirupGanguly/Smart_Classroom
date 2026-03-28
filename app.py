from flask import Flask, render_template

app = Flask(__name__)

# HOME PAGE 
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/upload_video")
def upload_video():
    return render_template("upload_video.html")


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


@app.route("/students_report")
def students_report():
    return render_template("students_report.html")


@app.route("/video_result")
def video_result():
    return render_template("video_result.html")


if __name__ == "__main__":
    app.run(debug=True)
