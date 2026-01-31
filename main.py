from fastapi import FastAPI

from voice import listen, speak
from vision import scan_environment
from navigation import navigate
from emergency import send_alert
from traffic import get_traffic_status

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Smart Path Running"}


def main_system():

    speak("Smart Path system activated")

    while True:

        command = listen()

        if "guide" in command:
            speak("Starting smart navigation")
            navigate()

        elif "traffic" in command:
            get_traffic_status()

        elif "scan" in command:
            scan_environment()

        elif "help" in command:
            send_alert()

        elif "where" in command:
            speak("Getting your location")

        elif "stop" in command:
            speak("System stopped")
            break


@app.get("/start")
def start():
    main_system()
    return {"status": "stopped"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

