from fastapi import WebSocket, APIRouter
from typing import List

# WebSocket Manager to manage active connections
class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("WebSocket connection established")

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("WebSocket connection closed")

    async def send_notification(self, message: str):
        """Send notifications to all connected clients."""
        for connection in self.active_connections:
            await connection.send_text(message)

# Initialize the WebSocketManager instance
ws_manager = WebSocketManager()

# WebSocket Router
websocket_router = APIRouter()

# WebSocket endpoint for receiving notifications
@websocket_router.websocket("/ws/notify")
async def websocket_endpoint(ws: WebSocket):
    # Connect the WebSocket
    await ws_manager.connect(ws)

    try:
        while True:
            # The WebSocket will listen for incoming messages if needed
            data = await ws.receive_text()
            print(f"Received message: {data}")  # Handle received message (optional)

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Disconnect WebSocket when done
        await ws_manager.disconnect(ws)

# Optional: Add a test endpoint to manually trigger notifications
@websocket_router.get("/send-notification")
async def send_notification():
    message = "This is a test notification!"
    await ws_manager.send_notification(message)
    return {"message": "Notification sent to all connected WebSocket clients."}
