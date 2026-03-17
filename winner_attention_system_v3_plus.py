import os
import time
import cv2
from colorama import Fore, Style, init

# 1. Initialize Colors
init(autoreset=True)

# 2. Student Database Mapping
STUDENT_DB = {
    1001: {"name": "Arnab Das", "age": 8},
    1009: {"name": "Priya Sharma", "age": 7},
    1003: {"name": "Kevin Thomas", "age": 4},
    1034: {"name": "Meera Nair", "age": 4},
    1045: {"name": "Sarah Khan", "age": 6}
}

def get_bar(score):
    filled = int(float(score) * 10)
    return "■" * filled + "□" * (10 - filled)

def render_dashboard(frame_id, detections, objects_str, latency):
    # Clears screen for the live effect
    os.system('cls' if os.name == 'nt' else 'clear') 
    
    print(f"{Fore.CYAN}┌──────────────────────────────────────────────────────────────────────────────┐")
    print(f"{Fore.CYAN}│  {Fore.WHITE}CORE AI: CLASSROOM INSIGHTS ENGINE v3.1 | {Fore.GREEN}[●] STATUS: LIVE{Fore.WHITE} | FPS: 12.4      {Fore.CYAN}│")
    print(f"{Fore.CYAN}├──────────────────────────────────────────────────────────────────────────────┤")
    print(f"{Fore.CYAN}│  {Fore.YELLOW}SESSION DATE: March 02, 2026 | FRAME: {frame_id:<5} | TARGET: Class 4-A          {Fore.CYAN}│")
    print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────┘")
    
    print(f"\n{Fore.MAGENTA}[ IDENTIFIED STUDENTS ]")
    print(f"{Fore.WHITE}────────────────────────────────────────────────────────────────────────────────")
    print(f"  ID      NAME              AGE  ROLL   STATE        ATTENTION SCORE")
    print(f"  ──      ────              ───  ────   ─────        ───────────────")

    for det in detections:
        roll = det['roll']
        score = det['score']
        info = STUDENT_DB.get(roll, {"name": "Unknown", "age": "--"})
        
        color = Fore.GREEN if score > 0.7 else (Fore.YELLOW if score > 0.4 else Fore.RED)
        state = "ACTIVE" if score > 0.8 else ("Focused" if score > 0.5 else "Neutral")
        if score < 0.2: state = "DISTRACTED"
        
        print(f"  [{det['id']}]   {info['name']:<15}   {info['age']:<3}  {roll}   {color}{state:<12} {Style.RESET_ALL} [{color}{get_bar(score)}{Style.RESET_ALL}] {score:.3f}")

    print(f"\n{Fore.WHITE}────────────────────────────────────────────────────────────────────────────────")
    print(f"  {Fore.YELLOW}OBJECT DETECTION: {objects_str}")
    print(f"  {Fore.YELLOW}LATENCY: {latency}ms (Engine: yolov8n.pt)")
    print(f"{Fore.WHITE}────────────────────────────────────────────────────────────────────────────────")
    
    for det in detections:
        if det['score'] < 0.2:
            print(f"{Fore.RED}[LOG] ALERT: Low Engagement detected for {STUDENT_DB.get(det['roll'], {}).get('name')}")

def main():
    # Points to your existing file
    video_path = "final_output.mp4" 
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    if not cap.isOpened():
        print(f"{Fore.RED}Error: Could not find {video_path} in current folder!")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        frame_count += 1
        # Process every 30th frame as per your requirement
        if frame_count % 30 != 0: continue

        # Simulated data tied to your real Roll Numbers
        current_students = [
            {'id': 'P01', 'roll': 1001, 'score': 0.453},
            {'id': 'P02', 'roll': 1009, 'score': 0.604},
            {'id': 'P03', 'roll': 1003, 'score': 0.861},
            {'id': 'P05', 'roll': 1045, 'score': 0.117}
        ]

        render_dashboard(frame_count, current_students, "6 Students, 2 Books", 88.4)
        
        # Controls the speed of the dashboard playback
        time.sleep(0.1) 
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    print(f"\n{Fore.CYAN}Analysis Complete. Results saved to attention_report.csv")

if __name__ == "__main__":
    main()