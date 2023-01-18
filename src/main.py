from client import Client
from server import Server

server = Server("192.168.150.126", 5003)
server.listen()
print("Server")
Client("192.168.150.126", 5002, "Aquino")
server.accept_connection()
server.accept_connection()
server.accept_connection()