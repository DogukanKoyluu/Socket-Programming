import socket
import threading

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, address, server):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.address = address
        self.server = server
        self.username = None
        self.connection_type = "TCP"

    def run(self):
        try:
            while True:
                self.client_socket.send("Kullanıcı adı girin: ".encode('utf-8'))
                username = self.client_socket.recv(1024).decode('utf-8').strip()

                if self.server.is_username_taken(username):
                    self.client_socket.send("Bu kullanıcı adı alınmış. Lütfen farklı bir kullanıcı adı girin.\n".encode('utf-8'))
                else:
                    self.username = username
                    break

            self.client_socket.send(f"Hoşgeldiniz, {self.username}! TCP ile bağlısınız.\n".encode('utf-8'))
            self.server.broadcast(f"{self.username} [{self.connection_type}] odaya katıldı.", None)
            self.server.add_client(self)

            while True:
                message = self.client_socket.recv(1024).decode('utf-8').strip()
                if not message or message.lower() == 'görüşürüz':
                    break
                self.server.broadcast(f"{self.username} [{self.connection_type}]: {message}", self.client_socket)
        except Exception as e:
            print(f"Error handling TCP message: {e}")
        finally:
            self.server.remove_client(self)
            self.server.broadcast(f"{self.username} [{self.connection_type}] odadan ayrıldı.", None)
            self.client_socket.close()

class UDPClientHandler(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.server = server
        self.address_user_map = {}

    def run(self):
        try:
            while True:
                message, address = self.server.udp_socket.recvfrom(1024)
                message = message.decode('utf-8').strip()

                if address not in self.address_user_map:
                    if ":" in message:
                        username = message.split(":")[0]
                    else:
                        username = message

                    if self.server.is_username_taken(username):
                        self.server.udp_socket.sendto("Bu kullanıcı adı alınmış. Lütfen farklı bir kullanıcı adı girin".encode('utf-8'), address)
                    else:
                        self.server.add_udp_client(username, address)
                        self.address_user_map[address] = username
                        self.server.udp_socket.sendto(f"Hoşgeldiniz, {username}! UDP ile bağlısınız.".encode('utf-8'), address)
                        self.server.broadcast(f"{username} [UDP] odaya katıldı.", None)
                else:
                    username = self.address_user_map[address]
                    if message.lower() == "görüşürüz":
                        self.server.remove_udp_client(username)
                        del self.address_user_map[address]
                        self.server.broadcast(f"{username} [UDP] odadan ayrıldı.", None)
                    else:
                        self.server.broadcast(f"{username} [UDP]: {message}", None, address)
        except Exception as e:
            print(f"Error handling UDP message: {e}")

class Server:
    def __init__(self):
        self.host = 'localhost'
        self.tcp_port = 12345
        self.udp_port = 12346
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clients = {}

    def set_up_server(self):
        self.tcp_socket.bind((self.host, self.tcp_port))
        self.tcp_socket.listen(5)
        print(f"TCP Server listening on port {self.tcp_port}")

        self.udp_socket.bind((self.host, self.udp_port))
        print(f"UDP Server listening on port {self.udp_port}")

        tcp_thread = threading.Thread(target=self.accept_tcp_connections)
        udp_thread = UDPClientHandler(self)

        tcp_thread.start()
        udp_thread.start()

    def accept_tcp_connections(self):
        try:
            while True:
                client_socket, address = self.tcp_socket.accept()
                client_handler = ClientHandler(client_socket, address, self)
                client_handler.start()
        except KeyboardInterrupt:
            print("TCP Server shutting down.")
        finally:
            self.tcp_socket.close()

    def add_client(self, client_handler):
        self.clients[client_handler.username] = {
            'address': client_handler.address,
            'socket': client_handler.client_socket,
            'type': client_handler.connection_type
        }

    def add_udp_client(self, username, address):
        self.clients[username] = {
            'address': address,
            'type': 'UDP'
        }

    def remove_client(self, client_handler):
        if client_handler.username in self.clients:
            del self.clients[client_handler.username]

    def remove_udp_client(self, username):
        if username in self.clients:
            del self.clients[username]

    def broadcast(self, message, from_socket=None, exclude_address=None):
        print(message)
        for client in self.clients.values():
            if client['type'] == 'UDP' and client['address'] != exclude_address:
                try:
                    self.udp_socket.sendto(message.encode('utf-8'), client['address'])
                except Exception as e:
                    print(f"Error sending UDP message: {e}")
            elif client['type'] == 'TCP' and client['socket'] != from_socket:
                try:
                    client['socket'].send(message.encode('utf-8'))
                except Exception as e:
                    print(f"Error sending TCP message: {e}")

    def is_username_taken(self, username):
        return username in self.clients

if __name__ == '__main__':
    server = Server()
    server.set_up_server()
