import socket
import threading

class SimpleServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.lock_holder = None

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client, address = self.sock.accept()
            print(f"New connection from {address}")
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                command, client_id = message.split(':')
                if command == "REQUEST_LOCK":
                    self.handle_lock_request(client, client_id)
                elif command == "RELEASE_LOCK":
                    self.handle_lock_release(client, client_id)
            except:
                if client in self.clients.values():
                    del self.clients[list(self.clients.values()).index(client)]
                client.close()
                break

    def handle_lock_request(self, client, client_id):
        if self.lock_holder is None:
            self.lock_holder = client_id
            self.clients[client_id] = client
            client.send("LOCK_GRANTED".encode('utf-8'))
            print(f"Lock granted to Client {client_id}")
        else:
            client.send("LOCK_DENIED".encode('utf-8'))
            print(f"Lock denied to Client {client_id}")

    def handle_lock_release(self, client, client_id):
        if client_id == self.lock_holder:
            self.lock_holder = None
            print(f"Lock released by Client {client_id}")

if __name__ == "__main__":
    server = SimpleServer('localhost', 5000)
    server.start()