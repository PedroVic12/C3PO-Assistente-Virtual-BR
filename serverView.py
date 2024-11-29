from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from c3po_gemini_api import AssistenteGenAI
from voice_assistente import TextToSpeech, OSystem
import speech_recognition as sr
import uuid

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize components
assistente = AssistenteGenAI()
tts = TextToSpeech()
os_helper = OSystem()

# Ensure static directories exist
os.makedirs('static/mp3', exist_ok=True)
os.makedirs('static/temp', exist_ok=True)

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.json
        user_input = data.get('user_input')
        voice_enabled = data.get('voice_enabled', False)
        
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400

        # Get response from Gemini
        response = assistente.responder(user_input)

        result = {'response': response}

        # Generate audio if voice is enabled
        if voice_enabled:
            audio_file = f"{uuid.uuid4()}.mp3"
            audio_path = os.path.join('static/mp3', audio_file)
            tts.text_to_speech(response, audio_path)
            result['audio_file'] = audio_file

        return jsonify(result)

    except Exception as e:
        print(f"Error in chatbot endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']
        temp_path = os.path.join('static/temp', f"{uuid.uuid4()}.wav")
        audio_file.save(temp_path)

        # Initialize recognizer
        r = sr.Recognizer()
        
        # Convert speech to text
        with sr.AudioFile(temp_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language='pt-BR')

        # Clean up temp file
        os.remove(temp_path)

        return jsonify({'text': text})

    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f'Error with the speech recognition service: {str(e)}'}), 500
    except Exception as e:
        print(f"Error in speech-to-text endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/static/mp3/<path:filename>')
def serve_audio(filename):
    return send_from_directory('static/mp3', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)