import socket
import threading

class UDPClient:
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = 'localhost'
        self.port = 12346
        self.username = None

    def set_username(self):
        while True:
            username = input("Kullanıcı adı girin: ").strip()
            if not username:
                print("Kullanıcı adı boş olamaz. Lütfen uygun kullanıcı adı girin.")
                continue
            self.udp_socket.sendto(username.encode('utf-8'), (self.host, self.port))
            response, _ = self.udp_socket.recvfrom(1024)
            if response.decode('utf-8') == "Bu kullanıcı adı alınmış. Lütfen farklı bir kullanıcı adı girin.":
                print(response.decode('utf-8'))
            else:
                self.username = username
                print(response.decode('utf-8'))
                break

    def start_client(self):
        self.set_username()

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        while True:
            message = input()
            if message.lower() == 'görüşürüz':
                self.udp_socket.sendto(f"{message}".encode('utf-8'), (self.host, self.port))
                break
            self.udp_socket.sendto(f"{message}".encode('utf-8'), (self.host, self.port))

        self.udp_socket.close()

    def receive_messages(self):
        try:
            while True:
                message, address = self.udp_socket.recvfrom(1024)
                decoded_message = message.decode('utf-8')
                if self.username and not decoded_message.startswith(f"{self.username}:"):
                    print(decoded_message)
        except Exception as e:
            print(f"Error receiving UDP message: {e}")

if __name__ == '__main__':
    client = UDPClient()
    client.start_client()
