import socket
import threading
from tkinter import messagebox

class PokerClient:
    def __init__(self, game_instance, host='127.0.0.1', port=1234):
        self.game = game_instance
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((host, port))
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "Could not connect to server")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message: break
                self.game.handle_server_message(message)
            except Exception as e:
                print(f"Connection error: {e}")
                break

    def send_action(self, action):
        try:
            self.client_socket.send(action.encode('utf-8'))
        except Exception as e:
            print(f"Failed to send action: {e}")