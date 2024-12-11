import time
import datetime
import pygame
import flet as ft
import os
from pathlib import Path

class AlarmClock:
    def __init__(self):
        self.sound_file = None
        self.is_running = False
        self.alarm_time = None
        pygame.mixer.init()

    def set_sound_file(self, file_path):
        """Define o arquivo de som para o alarme"""
        self.sound_file = file_path

    def stop_alarm(self):
        """Para o alarme"""
        self.is_running = False
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def start_alarm(self, alarm_time):
        """Inicia o alarme"""
        self.alarm_time = alarm_time
        self.is_running = True
        
        while self.is_running:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            if current_time == self.alarm_time:

                #! aqui melhor UX e UI
                print("WAKE UP! 😴")
                
                if self.sound_file and os.path.exists(self.sound_file):
                    pygame.mixer.music.load(self.sound_file)
                    pygame.mixer.music.play()
                    
                    while pygame.mixer.music.get_busy() and self.is_running:
                        time.sleep(1)
                
                self.is_running = False
            
            time.sleep(1)

def main(page: ft.Page):
    page.title = "C3PO Alarm Clock Jarvis 2024"
    page.theme_mode = "dark"
    page.padding = 20
    
    alarm = AlarmClock()
    
    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            alarm.set_sound_file(e.files[0].path)
            selected_file.value = f"Selected: {e.files[0].name}"
            page.update()

    def start_alarm_clicked(e):
        if not alarm.sound_file:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Please select a sound file first!"))
            )
            return
            
        time_str = f"{hour_drop.value}:{minute_drop.value}:{second_drop.value}"
        status_text.value = f"Alarm set for {time_str}"
        page.update()
        
        # Inicia o alarme em background
        import threading
        alarm_thread = threading.Thread(
            target=alarm.start_alarm, 
            args=(time_str,)
        )
        alarm_thread.daemon = True
        alarm_thread.start()

    def stop_alarm_clicked(e):
        alarm.stop_alarm()
        status_text.value = "Alarm stopped"
        page.update()

    # File picker
    file_picker = ft.FilePicker(
        on_result=pick_files_result,
    )
    page.overlay.append(file_picker)
    
    selected_file = ft.Text()
    
    # Time selection
    hours = [str(i).zfill(2) for i in range(24)]
    minutes = [str(i).zfill(2) for i in range(60)]
    seconds = [str(i).zfill(2) for i in range(60)]
    
    hour_drop = ft.Dropdown(
        label="Hour",
        width=100,
        options=[ft.dropdown.Option(hour) for hour in hours],
        value="00"
    )
    
    minute_drop = ft.Dropdown(
        label="Minute",
        width=100,
        options=[ft.dropdown.Option(minute) for minute in minutes],
        value="00"
    )
    
    second_drop = ft.Dropdown(
        label="Second",
        width=100,
        options=[ft.dropdown.Option(second) for second in seconds],
        value="00"
    )
    
    status_text = ft.Text(size=20)
    
    page.add(
        ft.Column(
            controls=[
                ft.Text("C3PO Alarm Clock", size=40, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Pick sound file",
                            icon=ft.icons.UPLOAD_FILE,
                            on_click=lambda _: file_picker.pick_files(
                                allow_multiple=False,
                                allowed_extensions=["mp3", "wav"]
                            )
                        ),
                    ]
                ),
                selected_file,
                ft.Row(
                    controls=[
                        hour_drop,
                        minute_drop,
                        second_drop,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Start Alarm",
                            icon=ft.icons.ALARM_ON,
                            on_click=start_alarm_clicked
                        ),
                        ft.ElevatedButton(
                            "Stop Alarm",
                            icon=ft.icons.ALARM_OFF,
                            on_click=stop_alarm_clicked
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                status_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
