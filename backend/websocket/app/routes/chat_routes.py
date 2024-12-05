from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.controllers.chat_controller import ChatController

router = APIRouter()
chat_controller = ChatController()

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    connection_id = await chat_controller.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            await chat_controller.handle_message(connection_id, data)
            
    except WebSocketDisconnect:
        chat_controller.disconnect(connection_id)
    except Exception as e:
        print(f"Error in websocket connection: {e}")
        chat_controller.disconnect(connection_id)

@router.get("/")
def index():
    return {"message": "Welcome to C3PO AI Assistant!"}