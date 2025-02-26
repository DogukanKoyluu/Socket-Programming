import socket
import threading

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        self.port = 12345

    def start_client(self):
        try:
            self.client_socket.connect((self.host, self.port))

            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()

            self.send_messages()
        except ConnectionRefusedError:
            print("Failed to connect to the server.")
        finally:
            self.client_socket.close()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8').strip()
                if not message:
                    break
                print(message)
            except ConnectionResetError:
                print("Disconnected from server.")
                break

    def send_messages(self):
        while True:
            message = input()
            if message.lower() == 'görüşürüz':
                self.client_socket.send(message.encode('utf-8'))
                break
            self.client_socket.send(message.encode('utf-8'))

if __name__ == '__main__':
    app = Client()
    app.start_client()
