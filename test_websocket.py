#!/usr/bin/env python3
"""
Simple WebSocket test client
Run this to test your WebSocket server
"""

import asyncio
import websockets
import json
import time

async def test_websocket():
    """Test the WebSocket server"""
    uri = "ws://localhost:8000/ws"
    
    try:
        print("🔌 Connecting to WebSocket server...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            
            # Wait for connection message
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📨 Received: {data}")
            
            # Send a test message
            test_message = {
                "type": "message",
                "message": "Hello from Python test client!",
                "timestamp": time.time()
            }
            
            print(f"📤 Sending: {test_message}")
            await websocket.send(json.dumps(test_message))
            
            # Wait for echo response
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📨 Echo received: {data}")
            
            # Wait for broadcast response
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📨 Broadcast received: {data}")
            
            print("✅ All tests passed!")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 Testing WebSocket Server")
    print("=" * 40)
    
    # Run the test
    result = asyncio.run(test_websocket())
    
    if result:
        print("🎉 WebSocket server is working correctly!")
    else:
        print("💥 WebSocket server test failed!")
        print("Make sure the server is running on ws://localhost:8000/ws") 