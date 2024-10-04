import socket

class Server:
    def __init__(self, protocol='TCP', ip='0.0.0.0', port=9999):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.server_socket = None

    def start(self):
        assert self.protocol in ['TCP', 'UDP'], "Unsupported protocol"
        assert isinstance(self.ip, str), "IP must be a string"
        assert isinstance(self.port, int), "Port must be an integer"

        if self.protocol == 'TCP': 
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        else:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.server_socket.bind((self.ip, self.port))

        self.server_socket.listen(5)
        print("Server listening on port", self.port)

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connected to {addr}")
            self._handle_client(client_socket)

    def _handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                print(f"Received: {data}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()
            print("Client disconnected")

    def close(self):
        if self.server_socket:
            print("Closing server socket")
            self.server_socket.close()
            self.server_socket = None

if __name__ == "__main__":
    server = Server()
    server.start()