import socket
import ssl

# Create an SSL context for a client
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

# Load the self-signed certificate
context.load_verify_locations(cafile="/home/nathaditya/Cryptography/SSL/server.crt")

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap the socket with SSL
ssl_socket = context.wrap_socket(client_socket, server_hostname='localhost')

# Connect to the server
ssl_socket.connect(('localhost', 4443))

# Receive data from the server
data = ssl_socket.recv(1024)
print(f"Received: {data.decode()}")

# Close the connection
ssl_socket.close()