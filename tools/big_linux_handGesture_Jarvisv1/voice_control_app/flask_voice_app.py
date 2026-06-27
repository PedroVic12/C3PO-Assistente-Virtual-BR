from flask import Flask, render_template, jsonify
import speech_recognition as sr
import pyttsx3
import threading
import time
from automation import LinuxCommands, AutomationControl

app = Flask(__name__)

class VoiceController:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.button_states = {
            'button1': False,
            'button2': False,
            'button3': False
        }
        # Inicializa as classes de automação
        self.linux_cmd = LinuxCommands()
        self.auto = AutomationControl()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def execute_command(self, command_number):
        """Executa comandos baseados no número"""
        if command_number == 1:
            self.auto.open_browser('brave')
            self.speak("Abrindo navegador Brave")
        elif command_number == 2:
            self.linux_cmd.switch_workspace_right()
            self.speak("Mudando área de trabalho para direita")
        elif command_number == 3:
            self.auto.open_github_desktop()
            self.speak("Abrindo GitHub Desktop")

    def listen_for_commands(self):
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source)
                    command = self.recognizer.recognize_google(audio, language='pt-BR').lower()
                    print(f"Recognized: {command}")

                    if "executar" in command:
                        if "um" in command or "1" in command:
                            self.button_states['button1'] = True
                            self.execute_command(1)
                        elif "dois" in command or "2" in command:
                            self.button_states['button2'] = True
                            self.execute_command(2)
                        elif "três" in command or "3" in command:
                            self.button_states['button3'] = True
                            self.execute_command(3)

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(0.1)

voice_controller = VoiceController()

@app.route('/')
def home():
    return render_template('voice_control.html')

@app.route('/toggle_listening')
def toggle_listening():
    voice_controller.is_listening = not voice_controller.is_listening
    if voice_controller.is_listening:
        threading.Thread(target=voice_controller.listen_for_commands, daemon=True).start()
    return jsonify({'is_listening': voice_controller.is_listening})

@app.route('/get_button_states')
def get_button_states():
    return jsonify(voice_controller.button_states)

@app.route('/reset_button/<button_id>')
def reset_button(button_id):
    if button_id in voice_controller.button_states:
        voice_controller.button_states[button_id] = False
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
