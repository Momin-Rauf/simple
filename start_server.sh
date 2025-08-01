#!/bin/bash

echo "🚀 Starting WebSocket Server..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

echo
echo "🎯 Starting server..."
echo "📡 WebSocket URL: ws://localhost:8000/ws"
echo "🌐 HTTP URL: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo
echo "💡 Open index.html in your browser to test"
echo

python3 start_server.py 