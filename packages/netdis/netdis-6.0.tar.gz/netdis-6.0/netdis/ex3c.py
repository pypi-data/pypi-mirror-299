import socket
import time
import random

class SimpleClient:
    def __init__(self, host, port, client_id):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id = client_id

    def start(self):
        self.sock.connect((self.host, self.port))
        print(f"Client {self.client_id} connected to server at {self.host}:{self.port}")

        while True:
            self.request_lock()
            time.sleep(random.uniform(1, 3))  # Wait before next request

    def request_lock(self):
        print(f"Client {self.client_id} requesting lock")
        self.sock.send(f"REQUEST_LOCK:{self.client_id}".encode('utf-8'))
        response = self.sock.recv(1024).decode('utf-8')
        
        if response == "LOCK_GRANTED":
            print(f"Client {self.client_id} granted lock. Entering critical section.")
            self.critical_section()
        else:
            print(f"Client {self.client_id} denied lock. Waiting...")

    def critical_section(self):
        print(f"Client {self.client_id} in critical section")
        time.sleep(random.uniform(1, 3))  # Simulate some work
        print(f"Client {self.client_id} exiting critical section")
        self.release_lock()

    def release_lock(self):
        self.sock.send(f"RELEASE_LOCK:{self.client_id}".encode('utf-8'))

if __name__ == "__main__":
    client_id = input("Enter client ID: ")
    client = SimpleClient('localhost', 5000, client_id)
    client.start()