from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="WebSocket Server", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
        
        # Send welcome message
        await websocket.send_text(json.dumps({
            "type": "connection",
            "message": "Connected to WebSocket server",
            "connections": len(self.active_connections)
        }))

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                # Remove broken connections
                if connection in self.active_connections:
                    self.active_connections.remove(connection)

manager = ConnectionManager()

@app.get("/")
async def root():
    return {
        "message": "WebSocket Server is running!",
        "status": "active",
        "connections": len(manager.active_connections)
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "connections": len(manager.active_connections)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            logger.info(f"Received message: {data}")
            
            try:
                # Try to parse as JSON
                message_data = json.loads(data)
                message_type = message_data.get("type", "message")
                message_content = message_data.get("message", data)
                
                # Echo back to sender
                response = {
                    "type": "echo",
                    "message": message_content,
                    "timestamp": message_data.get("timestamp")
                }
                await manager.send_personal_message(json.dumps(response), websocket)
                
                # Broadcast to all other clients
                broadcast_message = {
                    "type": "broadcast",
                    "message": message_content,
                    "connections": len(manager.active_connections)
                }
                await manager.broadcast(json.dumps(broadcast_message))
                
            except json.JSONDecodeError:
                # Handle plain text messages
                response = {
                    "type": "echo",
                    "message": data,
                    "error": "Invalid JSON format"
                }
                await manager.send_personal_message(json.dumps(response), websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # Notify other clients about the disconnection
        await manager.broadcast(json.dumps({
            "type": "disconnect",
            "message": "A client has disconnected",
            "connections": len(manager.active_connections)
        }))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 