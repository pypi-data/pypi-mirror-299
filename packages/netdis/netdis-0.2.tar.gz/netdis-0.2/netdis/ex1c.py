import socket
import pickle
import Pyro5.api

def socket_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 12345))
    print(pickle.loads(s.recv(4096)))
    s.close()

def rmi_client():
    remote_service = Pyro5.api.Proxy(Pyro5.api.locate_ns().lookup("example.remote_service"))
    print(remote_service.say_hello("RMI Client"))

if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Socket Communication")
        print("2. RMI Communication")
        print("3. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            socket_client()
        elif choice == '2':
            rmi_client()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
