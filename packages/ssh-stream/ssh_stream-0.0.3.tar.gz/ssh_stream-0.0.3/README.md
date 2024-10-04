# SSH-Stream 💻  ⇤⇥  ☁️
## Stream sensor data over ssh for real-time offboard computation

Do you have SSH access to a remote cluster with precious compute power and want to run a policy in the range of 5 Hz that is resource intensive?

### 1. Connect to your cluster via SSH
Choose a local port you want to forward to a remote port, e.g. `LOCAL_PORT = CLUSTER_PORT = 9999` and connect via ssh:
```
ssh -L LOCAL_PORT:localhost:CLUSTER_PORT user@cluster
```
### 2. Install the package and get your programs running
```
pip install ssh-stream
```
On the client (your robot @inference)

```python
from ssh_stream import Client
client = Client(port=9999)
client.connect()
while True:
  client.send("Hello World")
client.close()
```

On the cluster
```python
from ssh_stream import Server
server = Server(ip='0.0.0.0', port=9999)
server.start()
```





