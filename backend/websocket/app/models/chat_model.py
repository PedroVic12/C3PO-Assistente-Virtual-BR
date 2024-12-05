from typing import List, Dict
import google.generativeai as genai
from config.settings import settings

class ChatModel:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        
    def send_message(self, content: str) -> str:
        try:
            response = self.chat.send_message(content)
            return response.text
        except Exception as e:
            raise Exception(f"Error sending message: {str(e)}")

    def get_chat_history(self) -> List[Dict]:
        return [
            {"role": msg.role, "content": msg.parts[0].text}
            for msg in self.chat.history
        ]
