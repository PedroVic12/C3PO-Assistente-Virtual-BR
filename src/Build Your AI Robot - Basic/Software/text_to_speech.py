"""
Step 3: Text to Speech model
"""
import io
import pygame
from openai import OpenAI

client = OpenAI(api_key="sk-proj-GyXnA7wkEF0Euzt7WKhTT3BlbkFJsWytiP1LcfhC80pLtnAU")

# Function to play audio using pygame
def play_audio(audio_bytes):
    pygame.mixer.init()
    pygame.mixer.music.load(io.BytesIO(audio_bytes))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def openai_text_to_speech(text):
    # Generate speech
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input= text
    )
    # Extract audio content from the response
    audio_content = response.read()  # Read the binary content from the response
    return audio_content

# Play the audio
text = "Hi, I'm OpenAI's text to speech model"
response = openai_text_to_speech(text)
play_audio(response)

