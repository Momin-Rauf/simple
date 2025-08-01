# 🚀 Local WebSocket Setup Guide

This guide will help you set up and run the WebSocket server locally for simple text transfer.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Quick Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the Server

**Windows:**
```bash
start_server.bat
```

**Unix/Linux/Mac:**
```bash
chmod +x start_server.sh
./start_server.sh
```

**Manual:**
```bash
python start_server.py
```

### Step 3: Test the Connection

1. **Open `index.html`** in your web browser
2. **Wait for connection** (green dot should appear)
3. **Start typing messages** and click Send

## 🧪 Testing

### Test with Python Client
```bash
python test_websocket.py
```

### Test with Multiple Browser Tabs
1. Open `index.html` in multiple browser tabs
2. Send messages from different tabs
3. Watch real-time broadcasting between clients

## 📡 URLs

- **WebSocket**: `ws://localhost:8000/ws`
- **HTTP Server**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`

## 🔧 Troubleshooting

### Server Won't Start
- Check if Python is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check if port 8000 is available

### WebSocket Connection Fails
- Make sure the server is running
- Check browser console for errors
- Verify the URL in `index.html` is `ws://localhost:8000/ws`

### Messages Not Sending
- Check if the green connection dot is visible
- Open browser developer tools (F12) to see console messages
- Try refreshing the page

## 📁 Project Structure

```
simple/
├── main.py              # FastAPI WebSocket server
├── index.html           # WebSocket test client
├── requirements.txt     # Python dependencies
├── start_server.py      # Server startup script
├── start_server.bat     # Windows startup script
├── start_server.sh      # Unix startup script
├── test_websocket.py    # Python test client
├── render.yaml          # Render deployment config
└── README.md           # Project documentation
```

## 🎯 Features

✅ **Real-time messaging** - Instant message delivery  
✅ **Connection management** - Track active connections  
✅ **Message broadcasting** - Send to all connected clients  
✅ **Auto-reconnect** - Automatic reconnection on disconnect  
✅ **Modern UI** - Beautiful, responsive interface  
✅ **Cross-platform** - Works on Windows, Mac, Linux  

## 🚀 Next Steps

1. **Customize the UI** - Modify `index.html` styling
2. **Add features** - Extend `main.py` with new functionality
3. **Deploy to Render** - Use the `render.yaml` configuration
4. **Add authentication** - Implement user login/logout
5. **Add persistence** - Store messages in a database

## 💡 Tips

- **Multiple clients**: Open several browser tabs to test broadcasting
- **Network testing**: Try connecting from different devices on your network
- **Development**: The server auto-reloads when you modify `main.py`
- **Logs**: Check the terminal for server logs and connection info

Happy WebSocketing! 🎉 