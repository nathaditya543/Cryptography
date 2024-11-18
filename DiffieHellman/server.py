import socket
import random
# Set up server
HOST = '127.0.0.1' # localhost
PORT = 65432 # Port to listen on
p = int(input('Enter a prime number (p): '))
g = int(input('Enter a number (g): '))
class Server:
    def __init__(self, p, g):
        # server's private key (b)
        self.private_key = random.randint(1, p)
        self.p = p
        self.g = g
    def generate_public_key(self):
        # server's public key (g^b mod p)
        return (g**self.private_key) % p

    def compute_shared_secret(self, client_public_key):
        # Compute shared secret: (client_public_key^b mod p)
        return (client_public_key**self.private_key) % p
        
server = Server(p, g)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server is listening on {HOST}:{PORT}...')
    conn, addr = s.accept()

    with conn:
        print(f'Connected by {addr}')

        server_public_key = server.generate_public_key()
        conn.sendall(str(server_public_key).encode())
        print(f"Sent server's public key to Client: {server_public_key}")

        Client_public_key = int(conn.recv(1024).decode())
        print(f"Received Client's public key: {Client_public_key}")

        shared_secret = server.compute_shared_secret(Client_public_key)
        print(f"Shared secret computed by server: {shared_secret}")
        conn.sendall(f"Shared secret (server's perspective): {shared_secret}".encode())