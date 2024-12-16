from pydantic import BaseModel, ValidationError, Field
import pyautogui
import time

text = "Hello, my name is Manmay , how are you?"

from TTS.tts.configs.bark_config import BarkConfig
from TTS.tts.models.bark import Bark

config = BarkConfig()
model = Bark.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir="path/to/model/dir/", eval=True)

# with random speaker
output_dict = model.synthesize(text, config, speaker_id="random", voice_dirs=None)

# cloning a speaker.
# It assumes that you have a speaker file in `bark_voices/speaker_n/speaker.wav` or `bark_voices/speaker_n/speaker.npz`
output_dict = model.synthesize(text, config, speaker_id="ljspeech", voice_dirs="bark_voices/")

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio

# download and load all models
preload_models()
import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
wav = tts.tts(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en")
# Text to speech to a file
tts.tts_to_file(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")




# generate audio from text
text_prompt = """
     Hello, my name is Suno. And, uh — and I like pizza. [laughs] 
     But I also have other interests such as playing tic tac toe.
"""
audio_array = generate_audio(text_prompt)

# save audio to disk
write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
  
# play text in notebook
Audio(audio_array, rate=SAMPLE_RATE)



class MouseAction(BaseModel):
    x: int = Field(..., ge=0, description="Coordenada X do mouse, deve ser maior ou igual a zero.")
    y: int = Field(..., ge=0, description="Coordenada Y do mouse, deve ser maior ou igual a zero.")
    delay: float = Field(default=1.0, ge=0, description="Tempo de espera antes do clique, em segundos.")

class ScrollAction(BaseModel):
    direction: str = Field(..., regex="^(up|down)$", description="Direção do scroll: 'up' ou 'down'.")
    amount: int = Field(..., gt=0, description="Quantidade de scrolls a ser realizada.")

class MouseAutomation:
    @staticmethod
    def capture_coordinates():
        """Captura as coordenadas do mouse em tempo real."""
        print("Clique em qualquer lugar para capturar as coordenadas. Pressione Ctrl+C para sair.")
        try:
            while True:
                x, y = pyautogui.position()
                print(f"Posição atual do mouse: X={x}, Y={y}", end="\r", flush=True)
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nCaptura encerrada.")

    @staticmethod
    def click_button(action: MouseAction):
        """Move o mouse para as coordenadas especificadas e realiza um clique."""
        print(f"Movendo para X={action.x}, Y={action.y} com {action.delay}s de atraso e clicando...")
        pyautogui.moveTo(action.x, action.y, duration=action.delay)
        pyautogui.click()
        print("Clique realizado!")

    @staticmethod
    def scroll_page(action: ScrollAction):
        """Realiza o scroll na página na direção especificada."""
        if action.direction == "up":
            pyautogui.scroll(action.amount)
        elif action.direction == "down":
            pyautogui.scroll(-action.amount)
        print(f"Scroll realizado na direção '{action.direction}' com quantidade {action.amount}.")

# Exemplo de uso
if __name__ == "__main__":
    print("=== Automação com Mouse Iniciada ===")
    print("Escolha uma opção:")
    print("1. Capturar coordenadas do mouse")
    print("2. Realizar scroll")
    print("3. Clicar em um botão")
    print("4. Sair")

    while True:
        escolha = input("Digite sua escolha (1/2/3/4): ")

        if escolha == "1":
            MouseAutomation.capture_coordinates()
        elif escolha == "2":
            try:
                direction = input("Digite a direção do scroll ('up' ou 'down'): ").strip().lower()
                amount = int(input("Digite a quantidade de scrolls: "))
                scroll_action = ScrollAction(direction=direction, amount=amount)
                MouseAutomation.scroll_page(scroll_action)
            except ValidationError as e:
                print("Erro de validação:", e)
        elif escolha == "3":
            try:
                x = int(input("Digite a coordenada X do botão: "))
                y = int(input("Digite a coordenada Y do botão: "))
                delay = float(input("Digite o tempo de espera antes de clicar (em segundos): "))
                click_action = MouseAction(x=x, y=y, delay=delay)
                MouseAutomation.click_button(click_action)
            except ValidationError as e:
                print("Erro de validação:", e)
        elif escolha == "4":
            print("Encerrando o programa.")
            break
        else:
            print("Escolha inválida. Tente novamente.")

