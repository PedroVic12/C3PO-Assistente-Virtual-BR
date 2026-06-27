import flet as ft
import speech_recognition as sr
import pyttsx3
import threading
import time
import subprocess
import os

class VoiceControlApp:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.page = None
        self.scripts_dir = os.path.join(os.path.dirname(__file__), "executables")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def execute_script(self, script_number):
        script_path = os.path.join(self.scripts_dir, f"script{script_number}.py")
        if os.path.exists(script_path):
            subprocess.Popen(["/usr/bin/python3", script_path])
            return True
        return False

    def listen_for_command(self):
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source)
                    
                    command = self.recognizer.recognize_google(audio, language='pt-BR').lower()
                    print(f"Recognized: {command}")

                    if "executar" in command:
                        if "1" in command or "um" in command:
                            if self.execute_script(1):
                                self.page.client_storage.set("last_command", "Executar 1")
                                self.speak("Executando script um")
                        elif "2" in command or "dois" in command:
                            if self.execute_script(2):
                                self.page.client_storage.set("last_command", "Executar 2")
                                self.speak("Executando script dois")
                        elif "3" in command or "três" in command:
                            if self.execute_script(3):
                                self.page.client_storage.set("last_command", "Executar 3")
                                self.speak("Executando script três")
                        
                        self.page.update()

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
            except Exception as e:
                print(f"Error: {e}")

            time.sleep(0.1)

    def toggle_listening(self, e):
        self.is_listening = not self.is_listening
        if self.is_listening:
            self.page.floating_action_button.icon = ft.icons.MIC
            self.page.floating_action_button.bgcolor = ft.colors.RED_400
            threading.Thread(target=self.listen_for_command, daemon=True).start()
        else:
            self.page.floating_action_button.icon = ft.icons.MIC_OFF
            self.page.floating_action_button.bgcolor = ft.colors.BLUE_400
        self.page.update()

    def execute_button_click(self, script_number):
        def handle_click(e):
            if self.execute_script(script_number):
                self.page.client_storage.set("last_command", f"Executar {script_number}")
                self.speak(f"Executando script {script_number}")
                self.page.update()
        return handle_click

    def main(self, page: ft.Page):
        self.page = page
        page.title = "Controle por Voz"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        
        # Status text
        status_text = ft.Text(
            value="Clique no botão do microfone para começar",
            size=20,
            text_align=ft.TextAlign.CENTER,
        )

        # Command buttons
        btn1 = ft.ElevatedButton(
            text="Executar 1",
            width=200,
            height=50,
            style=ft.ButtonStyle(
                color={
                    ft.MaterialState.DEFAULT: ft.colors.WHITE,
                },
                bgcolor={
                    ft.MaterialState.DEFAULT: ft.colors.BLUE,
                },
            ),
            on_click=self.execute_button_click(1)
        )

        btn2 = ft.ElevatedButton(
            text="Executar 2",
            width=200,
            height=50,
            style=ft.ButtonStyle(
                color={
                    ft.MaterialState.DEFAULT: ft.colors.WHITE,
                },
                bgcolor={
                    ft.MaterialState.DEFAULT: ft.colors.GREEN,
                },
            ),
            on_click=self.execute_button_click(2)
        )

        btn3 = ft.ElevatedButton(
            text="Executar AÇÃO 3",
            width=200,
            height=50,
            style=ft.ButtonStyle(
                color={
                    ft.MaterialState.DEFAULT: ft.colors.WHITE,
                },
                bgcolor={
                    ft.MaterialState.DEFAULT: ft.colors.ORANGE,
                },
            ),
            on_click=self.execute_button_click(3)
        )

        # Container for buttons
        buttons_container = ft.Container(
            content=ft.Column(
                controls=[
                    btn1,
                    ft.Container(height=10),
                    btn2,
                    ft.Container(height=10),
                    btn3,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        )

        # Floating action button for voice control
        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.MIC_OFF,
            bgcolor=ft.colors.BLUE_400,
            on_click=self.toggle_listening,
        )

        # Add controls to page
        page.add(
            status_text,
            buttons_container,
        )

        def check_command():
            while True:
                last_command = page.client_storage.get("last_command")
                if last_command:
                    status_text.value = f"Último comando: {last_command}"
                    page.client_storage.remove("last_command")
                    page.update()
                time.sleep(0.1)

        threading.Thread(target=check_command, daemon=True).start()

if __name__ == "__main__":
    app = VoiceControlApp()
    ft.app(target=app.main)
