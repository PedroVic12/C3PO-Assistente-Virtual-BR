import os
from google.cloud import speech
from google.cloud import texttospeech
import wave
import pyaudio
from typing import Optional, List, Dict
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#docs
#https://cloud.google.com/python/docs/reference/speech/latest/google.cloud.speech_v1.services.speech.SpeechClient

class VoiceProcessor:
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize the VoiceProcessor with Google Cloud credentials
        
        Args:
            credentials_path: Path to Google Cloud credentials JSON file
        """
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        
        self.speech_client = speech.SpeechClient()
        self.tts_client = texttospeech.TextToSpeechClient()
        
        # Audio recording configuration
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.RECORD_SECONDS = 5
        
    def record_audio(self, output_file: str = "output.wav", duration: int = 5) -> str:
        """
        Record audio from microphone
        
        Args:
            output_file: Path to save the recorded audio
            duration: Recording duration in seconds
            
        Returns:
            Path to the recorded audio file
            
        Raises:
            PyAudioError: If there's an error initializing the audio stream
            IOError: If there's an error saving the audio file
        """
        self.RECORD_SECONDS = duration
        p = pyaudio.PyAudio()
        
        try:
            # List available input devices
            info = p.get_host_api_info_by_index(0)
            numdevices = info.get('deviceCount')
            input_device = None
            
            for i in range(0, numdevices):
                if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    device_info = p.get_device_info_by_host_api_device_index(0, i)
                    logger.info(f"Input Device {i}: {device_info.get('name')}")
                    if input_device is None:
                        input_device = i
            
            if input_device is None:
                raise RuntimeError("No input devices found")
                
            stream = p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                input_device_index=input_device,
                frames_per_buffer=self.CHUNK
            )
            
            logger.info("* Recording audio...")
            frames = []
            
            for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                try:
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    frames.append(data)
                except IOError as e:
                    logger.warning(f"Dropped frame due to overflow: {e}")
                    continue
                
            logger.info("* Done recording")
            
            stream.stop_stream()
            stream.close()
            
            # Save the recorded audio
            wf = wave.open(output_file, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            return output_file
            
        except Exception as e:
            logger.error(f"Error during audio recording: {e}")
            raise
        finally:
            p.terminate()
    
    def transcribe_file(self, speech_file: str, language_code: str = "pt-BR") -> List[Dict[str, str]]:
        """
        Transcribe audio file to text using Google Cloud Speech-to-Text
        
        Args:
            speech_file: Path to audio file
            language_code: Language code for transcription
            
        Returns:
            List of transcription results with confidence scores
        """
        try:
            with open(speech_file, "rb") as audio_file:
                content = audio_file.read()
            
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.RATE,
                language_code=language_code,
                enable_automatic_punctuation=True,
            )
            
            response = self.speech_client.recognize(config=config, audio=audio)
            
            results = []
            for result in response.results:
                alternative = result.alternatives[0]
                results.append({
                    "transcript": alternative.transcript,
                    "confidence": alternative.confidence
                })
                logger.info("Transcript: %s (Confidence: %f)", 
                          alternative.transcript, alternative.confidence)
            
            return results
            
        except Exception as e:
            logger.error("Error in transcription: %s", str(e))
            raise
    
    def text_to_speech(self, text: str, output_file: str = "output.mp3", 
                      language_code: str = "pt-BR", voice_name: str = "pt-BR-Standard-A",
                      speaking_rate: float = 1.0, pitch: float = 0.0) -> str:
        """
        Convert text to speech using Google Cloud Text-to-Speech
        
        Args:
            text: Text to convert to speech
            output_file: Path to save the audio file
            language_code: Language code for the voice
            voice_name: Name of the voice to use
            speaking_rate: Speaking rate, from 0.25 to 4.0
            pitch: Voice pitch, from -20.0 to 20.0
            
        Returns:
            Path to the generated audio file
        """
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=speaking_rate,
                pitch=pitch
            )
            
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            with open(output_file, "wb") as out:
                out.write(response.audio_content)
                
            logger.info("Audio content written to: %s", output_file)
            return output_file
            
        except Exception as e:
            logger.error("Error in text-to-speech conversion: %s", str(e))
            raise

def main():
    """
    Example usage of the VoiceProcessor class
    """
    # Initialize with your Google Cloud credentials
    processor = VoiceProcessor("path/to/your/credentials.json")
    
    try:
        # Record audio
        audio_file = processor.record_audio("test_recording.wav", duration=5)
        
        # Transcribe the recorded audio
        transcription = processor.transcribe_file(audio_file)
        print("Transcription results:", json.dumps(transcription, indent=2, ensure_ascii=False))
        
        # Convert the transcription back to speech
        if transcription:
            text = transcription[0]["transcript"]
            audio_output = processor.text_to_speech(text, "response.mp3")
            print(f"Response audio saved to: {audio_output}")
            
    except Exception as e:
        logger.error("Error in main process: %s", str(e))

if __name__ == "__main__":
    main()