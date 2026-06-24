#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse

# Try imports
try:
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    HAS_PYTTSX3 = False

try:
    from gtts import gTTS
    import tempfile
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False

class C3POVoiceAlerts:
    def __init__(self):
        pass

    def speak(self, text):
        print(f"🔊 C3PO: '{text}'")
        
        # Fallback 1: Native Linux spd-say (highly native, no library issues, supports pt-BR)
        if self._run_command(["which", "spd-say"]):
            try:
                # spd-say -l pt -t female1 "texto"
                subprocess.run(["spd-say", "-l", "pt", "-t", "female1", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except Exception:
                pass

        # Fallback 2: pyttsx3 (offline python TTS engine)
        if HAS_PYTTSX3:
            try:
                engine = pyttsx3.init()
                # Set language/voice if possible
                voices = engine.getProperty('voices')
                for voice in voices:
                    if 'portuguese' in voice.name.lower() or 'brazil' in voice.id.lower():
                        engine.setProperty('voice', voice.id)
                        break
                engine.setProperty('rate', 170)  # speaking speed
                engine.say(text)
                engine.runAndWait()
                return
            except Exception as e:
                print(f"[Aviso] pyttsx3 falhou: {e}")

        # Fallback 3: gTTS (Google TTS, requires internet but sounds premium)
        if HAS_GTTS:
            try:
                tts = gTTS(text=text, lang='pt')
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                    tts.save(f.name)
                    # Try players
                    for player in ["mpg123", "mpv", "play", "aplay"]:
                        if self._run_command(["which", player]):
                            subprocess.run([player, f.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            break
                os.unlink(f.name)
                return
            except Exception as e:
                print(f"[Aviso] gTTS falhou: {e}")

        # Fallback 4: espeak (often installed on linux)
        if self._run_command(["which", "espeak"]):
            try:
                subprocess.run(["espeak", "-v", "pt", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except Exception:
                pass

        print("❌ Nenhum mecanismo de síntese de voz disponível no sistema.")

    def _run_command(self, cmd_list):
        return subprocess.run(cmd_list, capture_output=True).returncode == 0

    def trigger_error(self):
        self.speak("Atenção mestre Pedro. Algo deu errado. Por favor, verifique os logs do sistema.")

    def trigger_fixing(self):
        self.speak("Iniciando rotinas de manutenção. Algo está funcionando e corrigindo as dependências agora.")

    def trigger_running(self):
        self.speak("Tudo pronto. Algo está rodando no terminal.")
        print("\n------------------------------------------------------------")
        answer = input("❓ Deseja ver a aplicação rodando para testar? (s/n) [padrão: s]: ").strip().lower()
        if answer in ["s", "sim", ""]:
            self.speak("Abrindo a aplicação para teste. Aguarde um instante.")
            # Open Brave browser pointing to local dashboard/api
            url = "http://localhost:5557"
            if self._run_command(["which", "brave"]):
                subprocess.Popen(["brave", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif self._run_command(["which", "xdg-open"]):
                subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                print(f"Abra no seu navegador: {url}")

def main():
    parser = argparse.ArgumentParser(description="Alertas de voz nativos do C3PO")
    parser.add_argument("state", choices=["error", "fixing", "running"], help="Estado do alerta de voz")
    args = parser.parse_args()

    alerts = C3POVoiceAlerts()
    if args.state == "error":
        alerts.trigger_error()
    elif args.state == "fixing":
        alerts.trigger_fixing()
    elif args.state == "running":
        alerts.trigger_running()

if __name__ == "__main__":
    main()
