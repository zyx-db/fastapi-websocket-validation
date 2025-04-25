from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from websocket_validation import WebSocketHandler, WebSocketMessage

app = FastAPI()
ws_handler = WebSocketHandler()

# Define your message payload models
class ChatMessage(BaseModel):
    message: str
    room_id: str

# Register a handler for chat messages
@ws_handler.register_handler("chat", ChatMessage)
async def handle_chat(websocket: WebSocket, payload: ChatMessage):
    await websocket.send_json({
        "type": "chat",
        "payload": {"message": f"Received: {payload.message}"}
    })

# Register the outgoing chat messages
ws_handler.register_outgoing_message_schema("chat", ChatMessage)

# Handle incoming messages
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        message = WebSocketMessage(**data)
        await ws_handler.dispatch(websocket, message)

# Get the schema for all message types
@app.get("/schema")
async def get_schema():
    return ws_handler.get_schema()