import socket
import time
import random

class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.logical_clock = 0
        self.vector_clock = [0, 0]  # [server, client]

    def send_message(self, clock_type):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            
            if clock_type == 'logical':
                self.logical_clock += 1
                message = f"logical:{self.logical_clock}"
            else:
                self.vector_clock[1] += 1
                message = f"vector:{self.vector_clock[1]}"

            s.sendall(message.encode())
            data = s.recv(1024).decode()
            
            received_type, received_time = data.split(':')
            received_time = int(received_time)

            if received_type == 'logical':
                self.logical_clock = max(self.logical_clock, received_time) + 1
                print(f"Updated Logical Clock: {self.logical_clock}")
            else:
                self.vector_clock[0] = max(self.vector_clock[0], received_time)
                self.vector_clock[1] += 1
                print(f"Updated Vector Clock: {self.vector_clock}")

    def run(self):
        for _ in range(10):
            clock_type = random.choice(['logical', 'vector'])
            self.send_message(clock_type)
            time.sleep(1)

if __name__ == "__main__":
    client = Client()
    client.run()