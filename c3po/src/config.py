"""Configuration module for the AI Assistant."""

import os

# API Configuration
API_KEY = "AIzaSyAxDCA2uS0OGqDZkaGJ0C-TNPQcllywwhg"
BASE_URL = "https://api.generativeai.google.com/v1beta2"
DEFAULT_MODEL = "gemini-1.5-pro-latest"
DEFAULT_VOICE = "pt-BR-Wavenet-A"

# Generation Configuration
GENERATION_CONFIG = {
    "temperature": 0.3,
    "top_k": 40,
    "top_p": 0.95,
    "candidate_count": 1,
}

# Safety Settings
SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]
