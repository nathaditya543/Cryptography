import socket
import ssl

# Create an SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to an address and port
server_socket.bind(('localhost', 4443))
server_socket.listen(5)
print("Server listening on port 4443...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} established!")

    # Wrap the accepted socket with SSL
    ssl_socket = context.wrap_socket(client_socket, server_side=True)

    ssl_socket.send(b"Hello, SSL Client!")
    ssl_socket.close()