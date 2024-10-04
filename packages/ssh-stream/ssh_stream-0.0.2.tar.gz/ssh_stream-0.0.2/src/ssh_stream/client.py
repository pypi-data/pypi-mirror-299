import socket
import signal
import sys
import time

class Client:
    def __init__(self, protocol='TCP', ip='localhost', port=9999):
        self.protocol = protocol
        self.ip = ip
        self.port = port
        self.client_socket = None

    def connect(self):
        assert self.protocol in ['TCP', 'UDP'], "Unsupported protocol"
        assert isinstance(self.ip, str), "IP must be a string"
        assert isinstance(self.port, int), "Port must be an integer"

        print("Creating socket object")
        if self.protocol == 'TCP':
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        def signal_handler(sig, frame):
            print("Closing socket")
            self.client_socket.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        try:
            print(f"Connecting to {self.ip}:{self.port}")
            self.client_socket.connect((self.ip, self.port))
            print("Connected successfully")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def send(self, data):
        assert self.client_socket is not None, "Client is not connected"
        assert isinstance(data, str), "Data must be a string"

        try:
            print(f"Sending data: {data}")
            self.client_socket.sendall(data.encode())
            print("Data sent successfully")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def close(self):
        if self.client_socket:
            print("Closing socket")
            self.client_socket.close()
            self.client_socket = None

if __name__ == "__main__":
    client = Client()
    if not client.connect():
        print("Failed to connect")
        exit(1)

    data = "Hello, world!"
    i = 0

    for i in range(len(data)):
        if not client.send(data[i]):
            print("Failed to send data")
            break

    client.close()

