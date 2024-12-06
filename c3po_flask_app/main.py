"""Main entry point for the AI Assistant application."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from src.ai_assistant import AIAssistant

app = Flask(__name__)
CORS(app)

assistant = AIAssistant()

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    data = request.json
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({
            "success": False,
            "response": "No message provided"
        }), 400
    
    response = assistant.respond(user_input)
    return jsonify(response)

@app.route('/process_image', methods=['POST'])
def process_image():
    """Handle image processing requests."""
    if 'image' not in request.files:
        return jsonify({
            "success": False,
            "response": "No image provided"
        }), 400
        
    image = request.files['image']
    prompt = request.form.get('prompt', '')
    
    # Save image to temporary location and process
    image_path = f"temp/{image.filename}"
    image.save(image_path)
    
    response = assistant.process_image(image_path, prompt)
    return jsonify(response)

@app.route('/process_file', methods=['POST'])
def process_file():
    """Handle file processing requests."""
    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "response": "No file provided"
        }), 400
        
    file = request.files['file']
    file_type = file.filename.split('.')[-1]
    
    # Save file to temporary location and process
    file_path = f"temp/{file.filename}"
    file.save(file_path)
    
    response = assistant.process_file(file_path, file_type)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=6000)
