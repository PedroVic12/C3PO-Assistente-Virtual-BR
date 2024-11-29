import os
import csv
import json
import datetime
import speech_recognition as sr
import pyttsx3
import uuid
from datetime import datetime

class TextToSpeech:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.setup_voice()
            self.base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'mp3')
            os.makedirs(self.base_path, exist_ok=True)
        except Exception as e:
            print(f"Error initializing text-to-speech: {str(e)}")
            self.engine = None

    def setup_voice(self):
        if not self.engine:
            return
            
        try:
            voices = self.engine.getProperty('voices')
            # Try to find a Portuguese voice
            pt_voice = None
            for voice in voices:
                if 'brazil' in voice.name.lower() or 'pt' in voice.name.lower():
                    pt_voice = voice
                    break
                    
            if pt_voice:
                self.engine.setProperty('voice', pt_voice.id)
            
            # Configure voice properties
            self.engine.setProperty('rate', 150)  # Speed
            self.engine.setProperty('volume', 1.0)  # Volume
        except Exception as e:
            print(f"Error setting up voice: {str(e)}")

    def text_to_speech(self, text):
        if not self.engine:
            print("Text-to-speech engine not initialized")
            return None
            
        try:
            # Generate unique filename
            filename = f"speech_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            filepath = os.path.join(self.base_path, filename)
            
            # Save audio to file
            self.engine.save_to_file(text, filepath)
            self.engine.runAndWait()
            
            # Verify file was created
            if os.path.exists(filepath):
                return filename
            else:
                print("Audio file was not created")
                return None
                
        except Exception as e:
            print(f"Error converting text to speech: {str(e)}")
            return None

class OSystem:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        os.makedirs(self.base_path, exist_ok=True)

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

    def speech_to_text(self, audio_path=None):
        try:
            if audio_path:
                with sr.AudioFile(audio_path) as source:
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