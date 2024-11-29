import os
import csv
import json
import datetime
import speech_recognition as sr
from elevenlabs import Voice, VoiceSettings, play, stream
from elevenlabs.client import ElevenLabs
import requests
import shutil
from pathlib import Path

class OSystem:
    def __init__(self):
        self.base_path = "/home/pedrov12/Documentos/GitHub/C3PO-Assistente-Virtual-BR/static"
        self.ensure_directories()
        self.recognizer = sr.Recognizer()

    def ensure_directories(self):
        """Ensure all necessary directories exist"""
        for dir_name in ['csv', 'txt', 'md', 'mp3']:
            Path(f"{self.base_path}/{dir_name}").mkdir(parents=True, exist_ok=True)

    def create_file(self, file_type, content, filename=None):
        """Create a file of specified type with given content"""
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"file_{timestamp}"

        file_path = f"{self.base_path}/{file_type}/{filename}.{file_type}"

        try:
            if file_type == 'csv':
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    if isinstance(content, list):
                        writer.writerows(content)
                    else:
                        writer.writerow([content])

            elif file_type in ['txt', 'md']:
                with open(file_path, 'w') as f:
                    f.write(content)

            elif file_type == 'mp3':
                # For MP3, content should be bytes or file-like object
                with open(file_path, 'wb') as f:
                    f.write(content)

            return file_path
        except Exception as e:
            print(f"Error creating {file_type} file: {e}")
            return None

    def delete_file(self, file_type, filename):
        """Delete a file of specified type"""
        file_path = f"{self.base_path}/{file_type}/{filename}.{file_type}"
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

    def list_files(self, file_type):
        """List all files of specified type"""
        directory = f"{self.base_path}/{file_type}"
        try:
            return [f for f in os.listdir(directory) if f.endswith(f".{file_type}")]
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    def speech_to_text(self, audio_file=None):
        """Convert speech to text from microphone or audio file"""
        try:
            if audio_file:
                with sr.AudioFile(audio_file) as source:
                    audio = self.recognizer.record(source)
            else:
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = self.recognizer.listen(source)
                    print("Processing...")

            text = self.recognizer.recognize_google(audio, language='pt-BR')
            return text
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None

class TextToSpeech:
    def __init__(self):
        self.API_KEY = "0c76ddcdc2d1aace04fda8e819f8b1ac"
        self.CHUNK_SIZE = 1024
        self.VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
        self.output_dir = "/home/pedrov12/Documentos/GitHub/C3PO-Assistente-Virtual-BR/static/mp3"

    def text_to_speech(self, text, filename=None):
        """Convert text to speech and save as MP3"""
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"speech_{timestamp}.mp3"

        output_path = os.path.join(self.output_dir, filename)

        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.VOICE_ID}/stream"
        headers = {
            "Accept": "application/json",
            "xi-api-key": self.API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }

        try:
            response = requests.post(tts_url, headers=headers, json=data, stream=True)
            if response.ok:
                with open(output_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                        f.write(chunk)
                print(f"Audio saved as: {output_path}")
                return output_path
            else:
                print(f"Error: {response.text}")
                return None
        except Exception as e:
            print(f"Error in text to speech conversion: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Initialize the systems
    os_system = OSystem()
    tts_system = TextToSpeech()

    while True:
        print("\nC3PO File System Menu:")
        print("1. Create file")
        print("2. Delete file")
        print("3. List files")
        print("4. Record speech and convert to text")
        print("5. Convert text to speech")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            file_type = input("Enter file type (csv/txt/md/mp3): ")
            if file_type in ['csv', 'txt', 'md']:
                content = input("Enter content: ")
                filename = input("Enter filename (optional, press enter to skip): ")
                if filename.strip():
                    path = os_system.create_file(file_type, content, filename)
                else:
                    path = os_system.create_file(file_type, content)
                print(f"File created at: {path}")

        elif choice == "2":
            file_type = input("Enter file type (csv/txt/md/mp3): ")
            print("\nAvailable files:")
            files = os_system.list_files(file_type)
            for i, file in enumerate(files, 1):
                print(f"{i}. {file}")
            if files:
                file_index = int(input("Enter file number to delete: ")) - 1
                if 0 <= file_index < len(files):
                    filename = files[file_index].rsplit('.', 1)[0]
                    if os_system.delete_file(file_type, filename):
                        print("File deleted successfully")
                    else:
                        print("Error deleting file")
                else:
                    print("Invalid file number")

        elif choice == "3":
            file_type = input("Enter file type (csv/txt/md/mp3): ")
            files = os_system.list_files(file_type)
            print(f"\nFiles in {file_type} directory:")
            for file in files:
                print(file)

        elif choice == "4":
            print("Recording... Speak now!")
            text = os_system.speech_to_text()
            if text:
                print(f"Recognized text: {text}")
                save = input("Do you want to save this text? (y/n): ")
                if save.lower() == 'y':
                    file_type = input("Enter file type to save (txt/md): ")
                    if file_type in ['txt', 'md']:
                        path = os_system.create_file(file_type, text)
                        print(f"Text saved to: {path}")

        elif choice == "5":
            text = input("Enter text to convert to speech: ")
            output_path = tts_system.text_to_speech(text)
            if output_path:
                print(f"Speech file created at: {output_path}")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")