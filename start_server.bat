@echo off
echo 🚀 Starting WebSocket Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Install dependencies if needed
echo 📦 Installing dependencies...
pip install -r requirements.txt

echo.
echo 🎯 Starting server...
echo 📡 WebSocket URL: ws://localhost:8000/ws
echo 🌐 HTTP URL: http://localhost:8000
echo 📖 API Docs: http://localhost:8000/docs
echo.
echo 💡 Open index.html in your browser to test
echo.

python start_server.py

pause 