import cv2
import requests
import geocoder
import time
from ultralytics import YOLO
from voice import speak


# Load YOLO model
model = YOLO("yolov8n.pt")


# Get live GPS location (IP based)
def get_live_location():

    g = geocoder.ip("me")

    if g.latlng:
        return g.latlng[1], g.latlng[0]  # (lon, lat)
    else:
        return None, None


# Get route from OSM + OSRM
def get_route(start_lon, start_lat, end_lon, end_lat):

    url = f"http://router.project-osrm.org/route/v1/walking/{start_lon},{start_lat};{end_lon},{end_lat}?overview=false&steps=true&geometries=geojson"

    res = requests.get(url)
    data = res.json()

    return data["routes"][0]["legs"][0]["steps"]


# Detect obstacles using camera
def detect_obstacles():

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    if not ret:
        speak("Camera not working")
        return

    results = model(frame)
    boxes = results[0].boxes

    if len(boxes) == 0:
        speak("Path is clear")
    else:
        for box in boxes:
            cls = int(box.cls[0])
            name = model.names[cls]
            speak(f"{name} ahead")

    cap.release()


# Turn by Turn Navigation
def start_navigation(end_lon, end_lat):

    speak("Getting your location")

    start_lon, start_lat = get_live_location()

    if start_lon is None:
        speak("Unable to get GPS location")
        return

    speak("Location detected. Calculating route")

    steps = get_route(
        start_lon, start_lat,
        end_lon, end_lat
    )

    speak("Navigation started")

    # Speak each step one by one
    for step in steps:

        maneuver = step["maneuver"]["type"]
        distance = int(step["distance"])
        name = step.get("name", "")

        if name:
            speak(f"{maneuver} on {name} for {distance} meters")
        else:
            speak(f"{maneuver} for {distance} meters")

        # Check obstacles during walking
        detect_obstacles()

        # Wait before next instruction
        time.sleep(5)

    speak("You have reached your destination")


# Destination (Change this place)
DEST_LAT = 12.9352   # Bangalore Example
DEST_LON = 77.6101


# Start System
start_navigation(DEST_LON, DEST_LAT)

