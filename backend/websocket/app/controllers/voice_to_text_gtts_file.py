from gtts import gTTS
#from pydub import AudioSegment
#from pydub.playback import play
from IPython.display import Audio, display
from pygame import mixer

import os


video_id = "12345"

with open(f"{video_id}-model_option.txt", "w") as text_file:
    text = "This  is a test."
    text_file.write(text)

def falar(text):
    tts = gTTS(text=text, lang='pt-br',     )
    tts.save('audio.mp3')
    mixer.init()
    mixer.music.load('audio.mp3')
    mixer.music.play()
    while mixer.music.get_busy():
        pass



def speak(text):
    tts = gTTS(text=text, lang='pt-br')
    tts.save('audio.mp3')
    return Audio('audio.mp3')
   


if __name__ == "__main__":
    falar("Hello, world!")
    falar("This is a test.")