import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 165)

recognizer = sr.Recognizer()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():

    with sr.Microphone() as source:

        speak("Listening")

        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            return text.lower()

        except:
            speak("Please repeat")
            return ""

