from ssh_stream import Client, Server

client = Client(ip='localhost', port=9999)

if not client.connect():
    print("Failed to connect")
    exit(1)

data = "Hello, world!"
i = 0

while True:
    if not client.send(data[i]):
        print("Failed to send data")
        break
    i += 1
    if i >= len(data): i = 0

client.close()



