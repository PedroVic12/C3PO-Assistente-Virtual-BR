from fastapi import WebSocket
import json
from typing import Dict, Any
import os
import google.generativeai as genai
import uuid

class C3poChatbotV3:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        if self.model:
            print("C3PO Gemini Pro model initialized successfully!")
        else:
            print("Error initializing the model.")
        self.chat = self.model.start_chat(history=[])
        
    def send_message(self, content: str) -> str:
        try:
            response = self.chat.send_message(content)
            return response.text
        except Exception as e:
            print(f"Error sending message: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"

class ChatController:
    def __init__(self):
        self.active_connections: Dict[str, tuple[WebSocket, C3poChatbotV3]] = {}
    
    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()
        connection_id = str(uuid.uuid4())
        self.active_connections[connection_id] = (websocket, C3poChatbotV3())
        return connection_id
    
    def disconnect(self, connection_id: str):
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
    
    async def handle_message(self, connection_id: str, message: Dict[str, Any]):
        if connection_id not in self.active_connections:
            return
            
        websocket, chatbot = self.active_connections[connection_id]
        try:
            content = message.get("content", "")
            if not content:
                await websocket.send_json({"error": "Message content is required"})
                return
                
            response = chatbot.send_message(content)
            await websocket.send_json({"response": response})
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "content": str(e)
            })
