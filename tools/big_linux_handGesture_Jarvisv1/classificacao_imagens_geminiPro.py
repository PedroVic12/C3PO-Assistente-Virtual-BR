import flet as ft
from flask import Flask, request, jsonify
import threading
import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
from database.mongodb_crud import MongoDBCRUD
from services.gemini_service import GeminiImageClassifier
import time
from datetime import datetime
import uuid

load_dotenv()

# Initialize Flask app
flask_app = Flask(__name__)
db = MongoDBCRUD()
gemini = GeminiImageClassifier()

# Initialize speech recognition and text-to-speech
engine = pyttsx3.init()
recognizer = sr.Recognizer()

class VoiceControlApp:
    def __init__(self):
        self.page = None
        self.is_listening = False
        self.storage_path = os.getenv('STORAGE_PATH', './storage')
        os.makedirs(self.storage_path, exist_ok=True)

    def speak(self, text: str):
        engine.say(text)
        engine.runAndWait()

    def process_image(self, image_path: str):
        try:
            # Classify image using Gemini
            result = gemini.classify_image(image_path)
            
            # Store result in MongoDB
            image_data = {
                "path": image_path,
                "classification": result,
                "timestamp": datetime.utcnow(),
                "status": "processed"
            }
            db.create("images", image_data)
            
            return result
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return {"error": str(e)}

    def handle_voice_command(self, command: str):
        try:
            if "classificar" in command.lower():
                # Get the latest image from storage
                images = os.listdir(self.storage_path)
                if images:
                    latest_image = sorted(images)[-1]
                    image_path = os.path.join(self.storage_path, latest_image)
                    self.speak("Classificando imagem...")
                    result = self.process_image(image_path)
                    self.speak("Imagem classificada com sucesso")
                    return result
                else:
                    self.speak("Nenhuma imagem encontrada")
                    return {"error": "No images found"}
            return {"error": "Unknown command"}
        except Exception as e:
            return {"error": str(e)}

    def listen_for_commands(self):
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio, language='pt-BR')
                    print(f"Command received: {command}")
                    result = self.handle_voice_command(command)
                    print(f"Command result: {result}")
            except Exception as e:
                print(f"Error in voice recognition: {str(e)}")
            time.sleep(0.1)

    def toggle_listening(self, e):
        self.is_listening = not self.is_listening
        if self.is_listening:
            threading.Thread(target=self.listen_for_commands, daemon=True).start()
            self.page.floating_action_button.bgcolor = ft.colors.RED_400
        else:
            self.page.floating_action_button.bgcolor = ft.colors.BLUE_400
        self.page.update()

    def build_ui(self, page: ft.Page):
        self.page = page
        page.title = "Classificador de Imagens por Voz"
        
        # Create UI components
        upload_button = ft.ElevatedButton(
            "Carregar Imagem",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: page.show_upload_dialog()
        )

        # Image display
        self.image_view = ft.Image(
            src=None,
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN,
        )

        # Results display
        self.results_text = ft.Text(
            value="Resultados aparecerão aqui",
            size=16,
            text_align=ft.TextAlign.LEFT,
        )

        # Main container
        main_content = ft.Column(
            controls=[
                ft.Text("Classificador de Imagens com IA", size=24, weight=ft.FontWeight.BOLD),
                upload_button,
                self.image_view,
                self.results_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        # Floating action button for voice control
        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.MIC,
            on_click=self.toggle_listening,
            bgcolor=ft.colors.BLUE_400,
        )

        page.add(main_content)

    def main(self, page: ft.Page):
        self.build_ui(page)

# Flask routes for API
@flask_app.route('/api/classify', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save file
    filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
    filepath = os.path.join(os.getenv('STORAGE_PATH'), filename)
    file.save(filepath)

    # Process with Gemini
    result = gemini.classify_image(filepath)
    
    # Store in MongoDB
    image_data = {
        "path": filepath,
        "classification": result,
        "timestamp": datetime.utcnow(),
        "status": "processed"
    }
    db.create("images", image_data)

    return jsonify(result)

def start_flask():
    flask_app.run(port=5000)

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # Start Flet app
    app = VoiceControlApp()
    ft.app(target=app.main)
