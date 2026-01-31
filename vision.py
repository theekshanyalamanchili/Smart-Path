import cv2
from ultralytics import YOLO
from voice import speak

model = YOLO("yolov8n.pt")


def scan_environment():

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    results = model(frame)

    boxes = results[0].boxes

    if len(boxes) == 0:
        speak("Path is clear")

    for box in boxes:

        cls = int(box.cls[0])
        name = model.names[cls]

        speak(f"{name} ahead")

    cap.release()

