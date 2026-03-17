import cv2
import os
import sys
import time
import numpy as np
from ultralytics import YOLO

# =========================
# VIDEO PATH (Command Line)
# =========================
if len(sys.argv) > 1:
    video_path = sys.argv[1]
else:
    print("Usage: python video_7_analysis.py <video_path>")
    sys.exit()

if not os.path.exists(video_path):
    print("Error: Video file not found.")
    sys.exit()

# =========================
# LOAD MODEL
# =========================
print("\nLoading YOLOv8 Nano Model (Intelligent Mode)...")
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error opening video.")
    sys.exit()

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# =========================
# OUTPUT VIDEO
# =========================
os.makedirs("output", exist_ok=True)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(
    "output/intelligent_output.mp4",
    fourcc,
    fps,
    (width, height)
)

# =========================
# VARIABLES
# =========================
CONF_THRESHOLD = 0.6   # 🔥 increase if needed (0.5–0.7 good range)

start_time = time.time()

frame_count = 0
person_detections = 0
unique_ids = set()

persons_per_frame = []
confidence_scores = []

student_entry = {}
student_last_seen = {}

peak_frame = 0
max_persons = 0

print("\n========== PROCESSING STARTED ==========\n")

# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    results = model.track(frame, persist=True, verbose=False)

    frame_ids = set()   # ✅ unique IDs per frame

    for r in results:
        if r.boxes.id is None:
            continue

        boxes = r.boxes.xyxy.cpu().numpy()
        ids = r.boxes.id.cpu().numpy()
        confs = r.boxes.conf.cpu().numpy()
        classes = r.boxes.cls.cpu().numpy()

        for box, track_id, conf, cls in zip(boxes, ids, confs, classes):

            # ✅ Only PERSON class + strong confidence
            if int(cls) == 0 and conf > CONF_THRESHOLD:

                frame_ids.add(int(track_id))
                unique_ids.add(int(track_id))
                confidence_scores.append(float(conf))
                person_detections += 1

                if track_id not in student_entry:
                    student_entry[track_id] = frame_count
                    print(f"Enrolled: Student_{int(track_id)} | Roll: {1000+int(track_id)}")

                student_last_seen[track_id] = frame_count

                x1, y1, x2, y2 = map(int, box)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame,
                            f"ID {int(track_id)}",
                            (x1, y1-5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0,255,0),
                            2)

    current_count = len(frame_ids)   # 🔥 FIXED COUNT
    persons_per_frame.append(current_count)

    if current_count > max_persons:
        max_persons = current_count
        peak_frame = frame_count

    cv2.putText(frame,
                f"Persons: {current_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                2)

    out.write(frame)

# =========================
# END PROCESSING
# =========================
cap.release()
out.release()

end_time = time.time()
processing_time = round(end_time - start_time, 2)

# =========================
# ANALYTICS
# =========================
avg_persons = round(np.mean(persons_per_frame), 2) if persons_per_frame else 0
avg_conf = round(np.mean(confidence_scores), 2) if confidence_scores else 0

stability = 100 - (np.std(persons_per_frame) * 10) if persons_per_frame else 0
stability = round(max(0, min(100, stability)), 2)

attendance_percent = []
for sid in student_entry:
    duration = student_last_seen[sid] - student_entry[sid]
    percent = (duration / frame_count) * 100
    attendance_percent.append(percent)

avg_attendance = round(np.mean(attendance_percent), 2) if attendance_percent else 0

# Density classification
if avg_persons < 4:
    density = "LOW"
elif avg_persons < 7:
    density = "MEDIUM"
else:
    density = "HIGH"

# Health grade
if stability > 85 and avg_conf > 0.8:
    grade = "A"
elif stability > 70:
    grade = "B"
else:
    grade = "C"

avg_fps = round(frame_count / processing_time, 2) if processing_time > 0 else 0

# =========================
# FINAL REPORT
# =========================
print("\n========== FINAL ADVANCED SUMMARY ==========\n")

print(f"Total Frames Processed: {frame_count}")
print(f"Total Unique Persons: {len(unique_ids)}")
print(f"Total Person Detections: {person_detections}")
print(f"Peak Crowd Frame: {peak_frame}")
print(f"Maximum Persons in a Frame: {max_persons}")
print(f"Average Persons per Frame: {avg_persons}")
print(f"Average Detection Confidence: {avg_conf}")
print(f"Detection Stability Score (%): {stability}")
print(f"Processing Time (seconds): {processing_time}")
print(f"Average FPS: {avg_fps}")

print("\n🏆 CLASSROOM HEALTH GRADE:", grade)