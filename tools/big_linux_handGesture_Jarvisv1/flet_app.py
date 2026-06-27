import flet as ft
import speech_recognition as sr
import pyttsx3
import threading
import time
from automation import LinuxCommands, AutomationControl

class ExerciseItem:
    def __init__(self, id, name, items):
        self.id = id
        self.name = name
        self.items = items

class VoiceController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
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
        elif command_number == 4:
            self.linux_cmd.switch_workspace_left()
            self.speak("Mudando área de trabalho para esquerda")

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
                            self.execute_command(1)
                        elif "dois" in command or "2" in command:
                            self.execute_command(2)
                        elif "três" in command or "3" in command:
                            self.execute_command(3)
                        elif "quatro" in command or "4" in command:
                            self.execute_command(4)

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(0.1)

def main(page: ft.Page):
    page.title = "Controle por Voz - Flet"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.spacing = 20
    
    # Inicializa o controlador de voz
    voice_controller = VoiceController(page)
    
    # Estado do microfone
    mic_status = ft.Text("Microfone Desativado", color=ft.colors.RED, size=16)
    
    def toggle_listening(e):
        voice_controller.is_listening = not voice_controller.is_listening
        if voice_controller.is_listening:
            mic_button.bgcolor = ft.colors.RED
            mic_button.text = "Desativar Microfone"
            mic_status.color = ft.colors.GREEN
            mic_status.value = "Microfone Ativado"
            threading.Thread(target=voice_controller.listen_for_commands, daemon=True).start()
        else:
            mic_button.bgcolor = ft.colors.BLUE
            mic_button.text = "Ativar Microfone"
            mic_status.color = ft.colors.RED
            mic_status.value = "Microfone Desativado"
        page.update()

    # Botão de microfone
    mic_button = ft.ElevatedButton(
        "Ativar Microfone",
        bgcolor=ft.colors.BLUE,
        color=ft.colors.WHITE,
        on_click=toggle_listening,
        width=200
    )

    # Título
    title = ft.Text("Controle por Voz", size=32, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("Comandos disponíveis:", size=16)

    # Lista de comandos
    commands = [
        "• 'executar um' ou 'executar 1': Abre o navegador Brave",
        "• 'executar dois' ou 'executar 2': Muda área de trabalho para direita",
        "• 'executar três' ou 'executar 3': Abre o GitHub Desktop",
        "• 'executar quatro' ou 'executar 4': Muda área de trabalho para esquerda",
    ]

    command_list = ft.Column(
        controls=[ft.Text(cmd, size=14) for cmd in commands],
        spacing=10
    )

    # Container principal
    main_container = ft.Container(
        content=ft.Column(
            controls=[
                title,
                ft.Divider(),
                ft.Row(
                    controls=[
                        mic_button,
                        mic_status,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(),
                subtitle,
                command_list,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=10,
    )

    # Adiciona o container à página
    page.add(main_container)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
