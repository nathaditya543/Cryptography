import socket
import random

HOST = '127.0.0.1'
PORT = 65432 
p = int(input('Enter the prime number (p): '))
g = int(input('Enter the number (g): '))
class Client:
    def __init__(self, p, g):
        # client's private key (a)
        self.private_key = random.randint(1, p)
        self.p = p
        self.g = g
        
    def generate_public_key(self):
        # client's public key (g^a mod p)
        return (g**self.private_key) % p
        
    def compute_shared_secret(self, server_public_key):
        # Compute shared secret: (server_public_key^a mod p)
        return (server_public_key**self.private_key) % p

client = Client(p, g)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    server_public_key = int(s.recv(1024).decode())
    print(f"Received Server's public key: {server_public_key}")
    client_public_key = client.generate_public_key()
    s.sendall(str(client_public_key).encode())
    print(f"Sent client's public key to Server: {client_public_key}")
    shared_secret = client.compute_shared_secret(server_public_key)
    print(f"Shared secret computed by Client: {shared_secret}")
    confirmation = s.recv(1024).decode()
    print(confirmation)
