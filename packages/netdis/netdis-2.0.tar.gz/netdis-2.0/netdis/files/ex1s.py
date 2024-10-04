import socket, pickle, Pyro5.api, threading

@Pyro5.api.expose
class RemoteService:
    def say_hello(self, name): return f"Hello, {name} from RMI!"

def start_rmi():
    daemon = Pyro5.api.Daemon()
    ns = Pyro5.api.locate_ns()
    ns.register("example.remote_service", daemon.register(RemoteService))
    daemon.requestLoop()

def start_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(1)
    while True:
        conn, _ = server.accept()
        conn.send(pickle.dumps({'message': 'Hello from Socket!'}))
        conn.close()

if __name__ == "__main__":
    threading.Thread(target=start_socket).start()
    threading.Thread(target=start_rmi).start()
