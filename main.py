from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WebSocket Test Client</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }

            .container {
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 600px;
                overflow: hidden;
            }

            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                text-align: center;
            }

            .header h1 {
                font-size: 24px;
                margin-bottom: 5px;
            }

            .status {
                font-size: 14px;
                opacity: 0.9;
            }

            .connection-status {
                display: inline-block;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                margin-right: 8px;
                background: #ff4757;
            }

            .connection-status.connected {
                background: #2ed573;
            }

            .messages {
                height: 400px;
                overflow-y: auto;
                padding: 20px;
                background: #f8f9fa;
            }

            .message {
                margin-bottom: 15px;
                padding: 12px 16px;
                border-radius: 10px;
                max-width: 80%;
                word-wrap: break-word;
            }

            .message.sent {
                background: #667eea;
                color: white;
                margin-left: auto;
                text-align: right;
            }

            .message.received {
                background: white;
                border: 1px solid #e9ecef;
                color: #333;
            }

            .message.system {
                background: #ffa502;
                color: white;
                text-align: center;
                max-width: 100%;
                font-size: 12px;
            }

            .message.error {
                background: #ff4757;
                color: white;
                text-align: center;
                max-width: 100%;
                font-size: 12px;
            }

            .message-type {
                font-size: 10px;
                opacity: 0.7;
                margin-bottom: 4px;
                text-transform: uppercase;
            }

            .input-area {
                padding: 20px;
                background: white;
                border-top: 1px solid #e9ecef;
            }

            .input-group {
                display: flex;
                gap: 10px;
            }

            .message-input {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #e9ecef;
                border-radius: 25px;
                font-size: 14px;
                outline: none;
                transition: border-color 0.3s;
            }

            .message-input:focus {
                border-color: #667eea;
            }

            .send-btn {
                padding: 12px 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
                transition: transform 0.2s;
            }

            .send-btn:hover {
                transform: translateY(-2px);
            }

            .send-btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }

            .stats {
                display: flex;
                justify-content: space-between;
                padding: 10px 20px;
                background: #f8f9fa;
                border-top: 1px solid #e9ecef;
                font-size: 12px;
                color: #666;
            }

            .clear-btn {
                background: none;
                border: none;
                color: #667eea;
                cursor: pointer;
                text-decoration: underline;
                font-size: 12px;
            }

            .clear-btn:hover {
                color: #764ba2;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>WebSocket Test Client</h1>
                <div class="status">
                    <span class="connection-status" id="connectionStatus"></span>
                    <span id="connectionText">Disconnected</span>
                </div>
            </div>

            <div class="stats">
                <span>Active Connections: <span id="connectionCount">0</span></span>
                <button class="clear-btn" onclick="clearMessages()">Clear Messages</button>
            </div>

            <div class="messages" id="messages"></div>

            <div class="input-area">
                <div class="input-group">
                    <input 
                        type="text" 
                        id="messageInput" 
                        class="message-input" 
                        placeholder="Type your message here..."
                        disabled
                    >
                    <button id="sendBtn" class="send-btn" onclick="sendMessage()" disabled>
                        Send
                    </button>
                </div>
            </div>
        </div>

        <script>
            // Auto-detect WebSocket URL for Render deployment
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const host = window.location.host;
            const WS_URL = `${protocol}//${host}/ws`;
            
            let ws = null;
            let messageCount = 0;

            // DOM elements
            const connectionStatus = document.getElementById('connectionStatus');
            const connectionText = document.getElementById('connectionText');
            const connectionCount = document.getElementById('connectionCount');
            const messages = document.getElementById('messages');
            const messageInput = document.getElementById('messageInput');
            const sendBtn = document.getElementById('sendBtn');

            // Initialize WebSocket connection
            function connect() {
                try {
                    ws = new WebSocket(WS_URL);
                    
                    ws.onopen = function(event) {
                        console.log('Connected to WebSocket server');
                        connectionStatus.classList.add('connected');
                        connectionText.textContent = 'Connected';
                        messageInput.disabled = false;
                        sendBtn.disabled = false;
                        addMessage('Connected to WebSocket server', 'system');
                    };

                    ws.onmessage = function(event) {
                        try {
                            const data = JSON.parse(event.data);
                            console.log('Received:', data);
                            
                            switch(data.type) {
                                case 'connection':
                                    addMessage(`Connected! Active connections: ${data.connections}`, 'system');
                                    connectionCount.textContent = data.connections;
                                    break;
                                case 'echo':
                                    addMessage(`Echo: ${data.message}`, 'received', data);
                                    break;
                                case 'broadcast':
                                    addMessage(`Broadcast: ${data.message}`, 'received', data);
                                    connectionCount.textContent = data.connections;
                                    break;
                                case 'disconnect':
                                    addMessage(`Client disconnected. Active connections: ${data.connections}`, 'system');
                                    connectionCount.textContent = data.connections;
                                    break;
                                default:
                                    addMessage(`Unknown message type: ${data.type}`, 'error');
                            }
                        } catch (e) {
                            addMessage(`Raw message: ${event.data}`, 'received');
                        }
                    };

                    ws.onclose = function(event) {
                        console.log('Disconnected from WebSocket server');
                        connectionStatus.classList.remove('connected');
                        connectionText.textContent = 'Disconnected';
                        messageInput.disabled = true;
                        sendBtn.disabled = true;
                        addMessage('Disconnected from WebSocket server', 'error');
                        
                        // Try to reconnect after 3 seconds
                        setTimeout(connect, 3000);
                    };

                    ws.onerror = function(error) {
                        console.error('WebSocket error:', error);
                        addMessage('WebSocket connection error', 'error');
                    };

                } catch (error) {
                    console.error('Failed to create WebSocket connection:', error);
                    addMessage('Failed to create WebSocket connection', 'error');
                }
            }

            // Send message function
            function sendMessage() {
                const message = messageInput.value.trim();
                if (message && ws && ws.readyState === WebSocket.OPEN) {
                    const data = {
                        type: 'message',
                        message: message,
                        timestamp: new Date().toISOString()
                    };
                    
                    ws.send(JSON.stringify(data));
                    addMessage(message, 'sent', data);
                    messageInput.value = '';
                    messageCount++;
                }
            }

            // Add message to the chat
            function addMessage(text, type, data = null) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${type}`;
                
                if (data && data.timestamp) {
                    const time = new Date(data.timestamp).toLocaleTimeString();
                    messageDiv.innerHTML = `
                        <div class="message-type">${type.toUpperCase()} - ${time}</div>
                        <div>${text}</div>
                    `;
                } else {
                    const time = new Date().toLocaleTimeString();
                    messageDiv.innerHTML = `
                        <div class="message-type">${type.toUpperCase()} - ${time}</div>
                        <div>${text}</div>
                    `;
                }
                
                messages.appendChild(messageDiv);
                messages.scrollTop = messages.scrollHeight;
            }

            // Clear messages
            function clearMessages() {
                messages.innerHTML = '';
            }

            // Handle Enter key
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            // Auto-connect when page loads
            window.addEventListener('load', function() {
                addMessage('WebSocket Test Client loaded. Connecting...', 'system');
                connect();
            });

            // Handle page unload
            window.addEventListener('beforeunload', function() {
                if (ws) {
                    ws.close();
                }
            });
        </script>
    </body>
    </html>
    """

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