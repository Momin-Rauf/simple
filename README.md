# FastAPI WebSocket Server

A simple WebSocket server built with FastAPI that can be deployed on Render.

## Features

- Real-time WebSocket communication
- Connection management
- Message broadcasting
- Health check endpoint
- CORS support
- JSON message handling

## Local Development

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

#### Option 1: Using the startup scripts (Recommended)

**Windows:**
```bash
start_server.bat
```

**Unix/Linux/Mac:**
```bash
chmod +x start_server.sh
./start_server.sh
```

#### Option 2: Manual startup

```bash
python start_server.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at:
- HTTP: http://localhost:8000
- WebSocket: ws://localhost:8000/ws

### Testing Locally

1. **Start the server** using one of the methods above
2. **Open `index.html`** in your web browser
3. **Start chatting!** The WebSocket connection will be established automatically

You can open multiple browser tabs with `index.html` to test real-time messaging between clients.

## API Endpoints

### HTTP Endpoints

- `GET /` - Server status and connection count
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)

### WebSocket Endpoint

- `WS /ws` - WebSocket connection endpoint

## WebSocket Message Format

### Sending Messages

Send JSON messages in this format:
```json
{
  "type": "message",
  "message": "Hello, World!",
  "timestamp": "2023-11-01T12:00:00Z"
}
```

### Receiving Messages

The server will respond with different message types:

1. **Connection Message** (when connecting):
```json
{
  "type": "connection",
  "message": "Connected to WebSocket server",
  "connections": 1
}
```

2. **Echo Message** (response to your message):
```json
{
  "type": "echo",
  "message": "Hello, World!",
  "timestamp": "2023-11-01T12:00:00Z"
}
```

3. **Broadcast Message** (sent to all other clients):
```json
{
  "type": "broadcast",
  "message": "Hello, World!",
  "connections": 2
}
```

4. **Disconnect Message** (when a client disconnects):
```json
{
  "type": "disconnect",
  "message": "A client has disconnected",
  "connections": 1
}
```

## Deployment on Render

### Option 1: Using render.yaml (Recommended)

1. Push your code to a Git repository
2. Connect your repository to Render
3. Render will automatically detect the `render.yaml` file and deploy your service

### Option 2: Manual Deployment

1. Create a new Web Service on Render
2. Connect your Git repository
3. Set the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python

## Testing the WebSocket

You can test the WebSocket connection using a simple HTML page or tools like:

- [WebSocket King](https://websocketking.com/)
- [Postman](https://www.postman.com/) (with WebSocket support)
- Browser's Developer Tools

### Simple HTML Test Client

Create an `index.html` file:

```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
</head>
<body>
    <h1>WebSocket Test</h1>
    <div id="messages"></div>
    <input type="text" id="messageInput" placeholder="Type a message...">
    <button onclick="sendMessage()">Send</button>

    <script>
        const ws = new WebSocket('ws://localhost:8000/ws');
        const messagesDiv = document.getElementById('messages');
        const messageInput = document.getElementById('messageInput');

        ws.onopen = function(event) {
            console.log('Connected to WebSocket');
        };

        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            const messageDiv = document.createElement('div');
            messageDiv.textContent = `${data.type}: ${data.message}`;
            messagesDiv.appendChild(messageDiv);
        };

        ws.onclose = function(event) {
            console.log('Disconnected from WebSocket');
        };

        function sendMessage() {
            const message = messageInput.value;
            if (message) {
                const data = {
                    type: 'message',
                    message: message,
                    timestamp: new Date().toISOString()
                };
                ws.send(JSON.stringify(data));
                messageInput.value = '';
            }
        }

        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
```

## Environment Variables

- `PORT` - Port number (automatically set by Render)

## License

MIT 