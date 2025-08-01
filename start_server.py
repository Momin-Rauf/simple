#!/usr/bin/env python3
"""
Simple startup script for the WebSocket server
Run this to start the server locally
"""

import uvicorn
import os
import sys

def main():
    print("🚀 Starting WebSocket Server...")
    print("=" * 50)
    print("📡 WebSocket URL: ws://localhost:8000/ws")
    print("🌐 HTTP URL: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("=" * 50)
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )

if __name__ == "__main__":
    main() 