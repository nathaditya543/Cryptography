import socket

def client():
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))
    data = ""
    while(data.lower().strip() != "exit"):
        data = input("Client: ")
        client_socket.send(data.encode())

        data = client_socket.recv(1024).decode()
        print("Server: " + str(data))

    client_socket.close()

if __name__ == "__main__":
    client()