"""
Step 3:
Text to Speech with offline library

"""
import pyttsx3

def text_to_speech(text, voice_index=0, rate=150, volume=1.0):
    """Convert text to speech using a specified voice."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Set properties
    engine.setProperty('voice', voices[voice_index].id)  # 0 male, 1 female
    engine.setProperty('rate', rate)  # Speech speed
    engine.setProperty('volume', volume)  # Volume (0.0 to 1.0)

    # Speak the text
    engine.say(text)
    engine.runAndWait()

# ---------------MAIN-----------------

# Input text and voice selection
text = "Hello, My name is emma, your personal AI robot!"
# Call the function
text_to_speech(text, rate=170, voice_index=1)
