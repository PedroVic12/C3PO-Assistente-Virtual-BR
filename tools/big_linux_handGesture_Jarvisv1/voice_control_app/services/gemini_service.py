from typing import Dict
import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv()

class ImageClassifierInterface(ABC):
    @abstractmethod
    def classify_image(self, image_path: str) -> Dict:
        pass

class GeminiImageClassifier(ImageClassifierInterface):
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro-vision')

    def classify_image(self, image_path: str) -> Dict:
        try:
            image = Image.open(image_path)
            
            prompt = """
            Please analyze this image and provide a detailed classification with the following information:
            1. Main subject or category
            2. Key features identified
            3. Confidence level (high, medium, low)
            4. Any relevant tags
            Format the response as a JSON object.
            """

            response = self.model.generate_content([prompt, image])
            
            # Clean and parse the response
            response_text = response.text
            # Note: In a real application, you'd want to properly parse this into a Dict
            # For now, we'll return a formatted dictionary
            return {
                "classification": response_text,
                "status": "success",
                "model": "gemini-pro-vision"
            }

        except Exception as e:
            return {
                "error": str(e),
                "status": "error",
                "model": "gemini-pro-vision"
            }

    def __del__(self):
        # Clean up any resources if needed
        pass
