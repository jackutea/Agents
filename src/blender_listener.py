import bpy
import socket
import threading
import json
import traceback

HOST = '127.0.0.1'
PORT = 8081

class BlenderSocketServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = False
        self.thread = None

    def handle_client(self, client_socket):
        with client_socket:
            while self.running:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    
                    payload = json.loads(data.decode('utf-8'))
                    command = payload.get('command', '')
                    
                    response = {"status": "success", "output": ""}
                    
                    if command:
                        try:
                            # ⚠️ Danger map: only for local restricted usage!
                            # exec can be dangerous if exposed
                            local_env = {"bpy": bpy}
                            exec(command, local_env)
                        except Exception as e:
                            response["status"] = "error"
                            response["output"] = traceback.format_exc()
                            
                    client_socket.sendall(json.dumps(response).encode('utf-8'))
                except json.JSONDecodeError:
                    pass
                except Exception as e:
                    print(f"Socket Handler Error: {e}")
                    break

    def _run(self):
        print(f"Blender Listener starting on {self.host}:{self.port}...")
        self.server_socket.settimeout(1.0)
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"Connected by {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.daemon = True
                client_thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Blender Listener Accept Error: {e}")

    def start(self):
        if self.running:
            print("Server is already running.")
            return
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()

# Global reference mapping to avoid Garbage Collection killing the server and for easy stop mapping
if "BS_SERVER" in locals():
    locals()["BS_SERVER"].stop()

BS_SERVER = BlenderSocketServer()
BS_SERVER.start()

print("Blender MCP Socket Server script executed. Waiting for commands on port", PORT)
