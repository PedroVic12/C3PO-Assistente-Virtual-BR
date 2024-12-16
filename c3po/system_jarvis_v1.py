from pydantic import BaseModel, ValidationError, Field
import pyautogui
import time
from TTS.tts.configs.bark_config import BarkConfig
from TTS.tts.models.bark import Bark
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio
import torch
from TTS.api import TTS

class TextToSpeech:
    @staticmethod
    def init_tts():
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        return tts

    @staticmethod
    def generate_audio_from_text(text: str, output_file: str):
        tts = TextToSpeech.init_tts()
        tts.tts_to_file(text=text, speaker_wav="my/cloning/audio.wav", language="en", file_path=output_file)
        print(f"Audio generated and saved to {output_file}")

    @staticmethod
    def bark_audio_generation(text: str):
        preload_models()
        audio_array = generate_audio(text)
        write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
        print("Bark audio generated and saved as 'bark_generation.wav'")
        return audio_array

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

class Main:
    @staticmethod
    def menu():
        print("=== Automação com Mouse Iniciada ===")
        print("Escolha uma opção:")
        print("1. Capturar coordenadas do mouse")
        print("2. Realizar scroll")
        print("3. Clicar em um botão")
        print("4. Gerar áudio com TTS")
        print("5. Gerar áudio com Bark")
        print("6. Sair")

        while True:
            escolha = input("Digite sua escolha (1/2/3/4/5/6): ")

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
                text = input("Digite o texto para sintetizar em áudio: ")
                output_file = input("Digite o caminho para salvar o áudio (ex: output.wav): ")
                TextToSpeech.generate_audio_from_text(text, output_file)
            elif escolha == "5":
                text = input("Digite o texto para gerar áudio com Bark: ")
                TextToSpeech.bark_audio_generation(text)
            elif escolha == "6":
                print("Encerrando o programa.")
                break
            else:
                print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    Main.menu()
