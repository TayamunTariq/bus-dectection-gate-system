# BusGuard: AI-Powered Automated Gate Entry System 🚌

## 📋 Overview
BusGuard is an IoT-ready computer vision system designed to automate security gates for educational institutions. By utilizing real-time object detection (YOLOv8), the system identifies approaching school buses and automatically triggers the gate opening mechanism, reducing wait times and manual labor for security personnel.

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Computer Vision:** OpenCV
* **AI Model:** YOLOv8 (You Only Look Once) - Pre-trained on COCO dataset
* **Hardware Simulation:** Mock GPIO triggering logic (Ready for Raspberry Pi/Jetson Nano integration)

## ⚙️ How It Works
1.  **Video Ingestion:** The system captures a live video feed from a webcam or IP camera.
2.  **Inference:** Frame-by-frame analysis is performed using the YOLOv8 Nano model.
3.  **Filtration:** The system filters detections specifically for `Class ID 5` (Bus) with a confidence threshold > 60%.
4.  **Action:** Upon positive identification, a signal is sent to the gate controller (simulated in code).

## 🚀 How to Run
1.  Clone the repository:
    ```bash
    git clone [https://github.com/yourusername/BusGuard.git](https://github.com/yourusername/BusGuard.git)
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the main script:
    ```bash
    python main.py
    ```
    *Note: The script uses the default webcam (0). To test with a video file, modify line 25 in `main.py`.*

## 🔮 Future Improvements
* Integration with OCR (EasyOCR) to read specific license plates.
* Deployment on edge devices like Raspberry Pi 4.
* Database logging for entry/exit times.