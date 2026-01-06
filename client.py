import socketio
import base64
import sys
if len(sys.argv) < 2:
    print("Usage: python client.py <base64_moduleArgs>")
    sys.exit(1)
moduleArgs = sys.argv[1]
decoded = base64.b64decode(moduleArgs).decode()
server_url, options = decoded.split('@@', 1)
print(f"Connecting to {server_url}")
sio = socketio.Client()
@sio.event
def connect():
    print("Connected to server")
@sio.event
def disconnect():
    print("Disconnected from server")
@sio.event
def receiver(data):
    print(f"Received: {data}")
    # Execute commands here
if __name__ == '__main__':
    try:
        sio.connect(server_url, transports=['polling', 'websocket'])
        sio.wait()
    except Exception as e:
        print(f"Connection failed: {e}")