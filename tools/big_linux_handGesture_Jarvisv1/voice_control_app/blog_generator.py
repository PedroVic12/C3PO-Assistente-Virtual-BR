from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import anthropic
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Anthropic client
client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))

def stream_response(messages):
    with client.messages.stream(
        model="claude-3-sonnet-20240229",
        max_tokens=4096,
        messages=messages,
        stream=True
    ) as stream:
        for text in stream:
            if hasattr(text, 'content'):
                yield f"data: {json.dumps({'content': text.content[0].text})}\n\n"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_post():
    data = request.json
    title = data.get('title', '')
    keywords = data.get('keywords', '')
    outline = data.get('outline', '')

    messages = [{
        "role": "user",
        "content": f"""Write a high-quality, SEO-optimized blog post. 
        Title: "{title}". 
        Keywords to target: {keywords}. 
        Outline/notes: {outline}. 
        Please write in a clear, engaging style with proper headings, paragraphs, and a conclusion. 
        Include relevant statistics when possible and make it informative yet easy to read.
        Format the post with appropriate HTML tags for web display."""
    }]

    return Response(
        stream_with_context(stream_response(messages)),
        content_type='text/event-stream'
    )

@app.route('/api/search')
def search():
    query = request.args.get('q', '')
    api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
    cx = os.getenv('GOOGLE_SEARCH_CX')
    
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cx,
        'q': query
    }
    
    try:
        response = requests.get(url, params=params)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
