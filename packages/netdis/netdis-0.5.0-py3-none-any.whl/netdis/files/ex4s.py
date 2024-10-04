import socket
import threading
import time

class Server:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.logical_clock = 0
        self.vector_clock = [0, 0]  # [server, client]

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Server listening on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn,))
                thread.start()

    def handle_client(self, conn):
        with conn:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                
                clock_type, received_time = data.split(':')
                received_time = int(received_time)

                if clock_type == 'logical':
                    self.logical_clock = max(self.logical_clock, received_time) + 1
                    print(f"Logical Clock: {self.logical_clock}")
                elif clock_type == 'vector':
                    self.vector_clock[1] = max(self.vector_clock[1], received_time)
                    self.vector_clock[0] += 1
                    print(f"Vector Clock: {self.vector_clock}")

                response = f"{clock_type}:{self.logical_clock if clock_type == 'logical' else self.vector_clock[0]}"
                conn.sendall(response.encode())

if __name__ == "__main__":
    server = Server()
    server.start()