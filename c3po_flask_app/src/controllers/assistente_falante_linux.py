import google.generativeai as genai
import speech_recognition as sr
import logging
from colorama import Fore, Style, init
from comando_linux import CommandFactory
import re
import os
from gtts import gTTS
from pygame import mixer
import pyautogui
import selenium


# Initialize colorama for colored terminal output
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class VoiceAssistant:
    def __init__(self, api_key: str):
        self.setup_gemini(api_key)
        self.setup_speech_recognition()
        self.command_patterns = {
            r"abrir (navegador|chrome|firefox)(?:\s+com\s+(.+))?": ("browser", "handle"),
            r"área de trabalho (direita|esquerda)": ("workspace", "handle"),
            r"executar programa (.+)": ("run", "handle"),
            r"(aumentar|diminuir|mudo) volume": ("system", "handle"),
            r"buscar notícias(?:\s+sobre\s+(.+))?": ("news", "handle"),
        }

    def menu_comando_porVoz(self, comando = 1):
        


        if comando == 1:
            print("Comandos disponiveis:")
            for pattern, (handler_type, method) in self.command_patterns.items():
                print(f"{pattern}: {handler_type} {method}")
            
        elif comando == 2:
            print("Comando 2")
            #abir navegador com url

            self.falar_voice_google("Qual url deseja abrir?")
            url = input('Coloque a url:')
            self.falar_voice_google(f"Abrindo navegador com {url}")
            webbrowser.open(url)


        elif comando == 3:
            print("Comando 3")
            #botao no tecaldo ctrl + alt + seta direita

            pyautogui.keyDown('ctrl')
            pyautogui.keyDown('alt')
            pyautogui.keyDown('right')
            pyautogui.keyUp('right')
            pyautogui.keyUp('alt')
            pyautogui.keyUp('ctrl')

        elif comando == 4:
            print("Comando 4")
            #botao no tecaldo ctrl + alt + seta esquerda

            pyautogui.keyDown('ctrl')
            pyautogui.keyDown('alt')
            pyautogui.keyDown('left')


        elif comando == 5:
            print("Comando 5")
            #botao no tecaldo ctrl + alt + seta cima

            pyautogui.keyDown('win')
            pyautogui.write("Big Store")
            pyautogui.press('enter')
    
    def falar_voice_google(self,text):
        tts = gTTS(text=text, lang='pt-br',     )
        tts.save('./audio.mp3')
    
        mixer.init()
        mixer.music.load('./audio.mp3')
        mixer.music.play()
        while mixer.music.get_busy():
            pass
        mixer.music.stop()
        mixer.quit()

    def setup_gemini(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        logging.info(f"{Fore.CYAN}Gemini AI configurado com sucesso{Style.RESET_ALL}")


    def setup_speech_recognition(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        logging.info(f"{Fore.GREEN}Reconhecimento de voz configurado{Style.RESET_ALL}")


    def listen(self) -> str:
        with self.microphone as source:
            os.system("clear")

            logging.info(f"\n\n\n{Fore.YELLOW}Ouvindo...{Style.RESET_ALL}")
            audio = self.recognizer.listen(source)
            self.menu_comando_porVoz()

            try:
                text = self.recognizer.recognize_google(audio, language="pt-BR")
                logging.info(f"{Fore.GREEN}Você disse: {text}{Style.RESET_ALL}")
                #print("VOCE", text)
                return text.lower()
            except Exception as e:
                logging.error(f"{Fore.RED}Erro ao reconhecer áudio: {e}{Style.RESET_ALL}")
                return ""

    def process_command(self, text: str):
        for pattern, (handler_type, method) in self.command_patterns.items():
            match = re.match(pattern, text)
            if match:
                handler = CommandFactory.get_handler(handler_type)
                if handler:
                    args = match.groups()[1] if len(match.groups()) > 1 else match.groups()[0]
                    getattr(handler, method)(args)
                    return True
        return False

    def chat_with_gemini(self, text: str) -> str:
        try:
            response = self.chat.send_message(text)
            return response.text
        except Exception as e:
            logging.error(f"{Fore.RED}Erro ao processar com Gemini: {e}{Style.RESET_ALL}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem."

    def run(self):
        self.falar_voice_google("\nOlá! Eu sou o C3PO, seu assistente pessoal. Como posso ajudar?")
        
        ligar_mic = True
        
        while True:


            self.menu_comando_porVoz()
            if ligar_mic:
                self.falar_voice_google("O que deseja?")
                text = self.listen()

                if not text:
                    continue
                    
                if text == "desligar":
                    self.speak("Até logo!")
                    break
        
            else:
                texto = input("Escreva sua mensagem (ou #sair): ")


            # Primeiro tenta processar como comando
            if not self.process_command(text):
                # Se não for um comando, usa o Gemini para resposta
                response = self.chat_with_gemini(text)
                self.falar_voice_google(response)
                logging.info(f"\n\n{Fore.BLUE}C3PO Gemini Assistente 2024: {response}{Style.RESET_ALL}")

def main():
    assistant = VoiceAssistant("AIzaSyD0m95XOFOADOQg1Ul_XFciPPmqytrCwdI")
    assistant.run()

if __name__ == '__main__':
    main()