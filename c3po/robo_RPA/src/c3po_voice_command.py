# voice_commands.py
import speech_recognition as sr
import pyttsx3
import os

class VoiceCommands:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def speak(self, message):
        self.engine.say(message)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            os.system("clear")
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                print(f"Command recognized: {command}")
                return command.lower()
            except Exception as e:
                print("Sorry, I didn't catch that.")
                return None
