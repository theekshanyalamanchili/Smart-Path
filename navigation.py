from voice import speak
from traffic import get_traffic_status


def navigate():

    speak("Checking traffic conditions")

    get_traffic_status()

    steps = [
        "Go straight for 50 meters",
        "Turn left",
        "Cross carefully",
        "Turn right",
        "Destination reached"
    ]

    for step in steps:
        speak(step)

