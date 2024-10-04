import socket
import time
import random

class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.logical_clock = 0
        self.vector_clock = [0, 0]  # [server, client]

    def send_message(self, message, clock_type):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            
            if clock_type == 'logical':
                self.logical_clock += 1
                message_to_send = f"{message}:logical:{self.logical_clock}"
            else:
                self.vector_clock[1] += 1
                message_to_send = f"{message}:vector:{self.vector_clock[1]}"

            # Send message along with clock type and value to the server
            s.sendall(message_to_send.encode())
            
            # Receive the updated clock value from the server
            data = s.recv(1024).decode()
            received_type, received_time = data.split(':')
            received_time = int(received_time)

            # Update the client's clocks based on the server's response
            if received_type == 'logical':
                self.logical_clock = max(self.logical_clock, received_time) + 1
                print(f"Client Logical Clock updated: {self.logical_clock}")
            else:
                self.vector_clock[0] = max(self.vector_clock[0], received_time)
                self.vector_clock[1] += 1
                print(f"Client Vector Clock updated: {self.vector_clock}")

    def run(self):
        messages = ["Hello", "How are you?", "What's up?", "Goodbye"]
        
        for _ in range(5):
            message = random.choice(messages)
            clock_type = random.choice(['logical', 'vector'])
            print(f"Sending message: '{message}' with {clock_type} clock")
            self.send_message(message, clock_type)
            time.sleep(1)

if __name__ == "__main__":
    client = Client()
    client.run()
