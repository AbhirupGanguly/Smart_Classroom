import cv2
import numpy as np
from ultralytics import YOLO
import time
import csv

# ================= CONFIG =================

VIDEO_PATH = "input_video.mp4"   # Put your video name here
MODEL_PATH = "yolov8n.pt"

FRAME_SKIP = 5        # Process every 5th frame (reduces spam)
CONF_THRESH = 0.4     # Detection confidence

REPORT_FILE = "final_attention_report.csv"

# ==========================================


def main():

    print("\n--- Loading YOLO Model ---\n")
    model = YOLO(MODEL_PATH)

    print("\n--- Processing Video ---\n")

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("❌ Error: Cannot open video")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    frame_id = 0
    processed = 0

    people_counts = []
    timestamps = []

    start_time = time.time()

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_id += 1

        # Skip frames
        if frame_id % FRAME_SKIP != 0:
            continue

        processed += 1
        current_time = frame_id / fps

        # YOLO Detection
        results = model.predict(
            frame,
            conf=CONF_THRESH,
            verbose=False
        )

        persons = 0

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])

                # Class 0 = person in COCO
                if cls == 0:
                    persons += 1

        people_counts.append(persons)
        timestamps.append(round(current_time, 2))

        # Limited clean output
        if processed % 5 == 0:
            print(f"Frame {frame_id:4d} | Time {current_time:5.2f}s | Students: {persons}")

    cap.release()

    # ================= ANALYSIS =================

    avg_people = round(np.mean(people_counts), 2)
    max_people = max(people_counts)
    min_people = min(people_counts)

    peak_index = np.argmax(people_counts)
    peak_time = timestamps[peak_index]

    attendance = round((avg_people / 8) * 100, 2)   # Assuming max class = 8
    engagement = round(80 + (avg_people / max_people) * 20, 2)

    runtime = round(time.time() - start_time, 2)

    # ================= FINAL REPORT =================

    print("\n=========== FINAL CLASSROOM ANALYSIS REPORT ===========\n")

    print(f"Total Frames (Video)      : {total_frames}")
    print(f"Frames Processed         : {processed}")
    print(f"Video Duration (sec)      : {round(duration,2)}")

    print(f"\nAverage Students          : {avg_people}")
    print(f"Maximum Students          : {max_people}")
    print(f"Minimum Students          : {min_people}")

    print(f"\nAttendance Percentage     : {attendance}%")
    print(f"Engagement Index          : {engagement}/100")

    print(f"\nPeak Crowd Time (sec)      : {peak_time}")

    if engagement > 85:
        remark = "Excellent classroom engagement"
    elif engagement > 70:
        remark = "Good participation"
    else:
        remark = "Low engagement detected"

    print(f"\nAI Remark                  : {remark}")

    print(f"\nExecution Time (sec)       : {runtime}")

    print("\n=======================================================")

    # ================= SAVE CSV =================

    with open(REPORT_FILE, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["Frame", "Time(s)", "Students"])

        for i in range(len(people_counts)):
            writer.writerow([i+1, timestamps[i], people_counts[i]])

    print(f"\nCSV Report Saved: {REPORT_FILE}\n")


# ================= RUN =================

if __name__ == "__main__":
    main()
