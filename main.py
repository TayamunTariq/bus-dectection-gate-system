import cv2
from ultralytics import YOLO
import time

# --- CONFIGURATION ---
CONFIDENCE_THRESHOLD = 0.6  # 60% confidence required
CLASS_ID_BUS = 5            # YOLO COCO dataset ID for 'bus' is 5
GATE_COOLDOWN = 10          # Seconds to wait before triggering gate again

# --- MOCK HARDWARE FUNCTION ---
def open_gate():
    """
    Simulates sending a signal to a microcontroller (e.g., Arduino/ESP32)
    to open the physical gate.
    """
    print("\n[GPIO ACTION] 🟢 RELAY TRIGGERED: GATE OPENING...")
    print("[SYSTEM] Waiting for vehicle to pass...\n")
    # In a real scenario, you would use: GPIO.output(PIN, GPIO.HIGH)

def main():
    # 1. Load the YOLOv8 model (Nano version for speed)
    print("[INIT] Loading AI Model...")
    model = YOLO("yolov8n.pt") 

    # 2. Initialize Video Stream (0 for Webcam, or put "video.mp4" for a file)
    cap = cv2.VideoCapture(0) # Change to filename if you don't want to use webcam
    
    # Track the last time the gate was opened
    last_open_time = 0

    if not cap.isOpened():
        print("[ERROR] Could not open video source.")
        return

    print("[SYSTEM] Surveillance Active. Waiting for buses...")

    while True:
        success, frame = cap.read()
        if not success:
            break

        # 3. AI Inference: Run detection on the current frame
        # stream=True makes it faster for video
        results = model(frame, stream=True, verbose=False)

        bus_detected = False

        # 4. Process Results
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Check class and confidence
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])

                if cls_id == CLASS_ID_BUS and conf > CONFIDENCE_THRESHOLD:
                    bus_detected = True
                    
                    # Draw bounding box on the screen (Visual Feedback)
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"SCHOOL BUS: {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 5. Logic Control: Open gate if bus found + cooldown is over
        current_time = time.time()
        if bus_detected:
            if current_time - last_open_time > GATE_COOLDOWN:
                open_gate()
                last_open_time = current_time
                # Visual indicator on screen
                cv2.putText(frame, "GATE OPENING", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # 6. Display the Surveillance Feed
        cv2.imshow("BusGuard AI Feed", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()