import socket
import hashlib


def verify_sig(s1,s2,message, pub_key):
    p = pub_key[0]
    alpha = pub_key[1]
    y = pub_key[2]

    hash_object = hashlib.sha256(message.encode())
    m = int(hash_object.hexdigest(), 16)%p

    v1 = pow(alpha, m) % p
    v2 = (pow(y,s1)*pow(s1,s2)) % p

    return v1 == v2


def server():
    server_socket = socket.socket()
    host = '127.0.0.1'
    port = 5000

    server_socket.bind((host, port))
    server_socket.listen(1)
    conn, address = server_socket.accept()

    print(f"Connection from {address}")

    pub_str = conn.recv(1024).decode()
    pub_key = []
    for i in pub_str.split("#"):
        pub_key.append(int(i))
    

    while(True):
        data = conn.recv(1024).decode()
        if not data:
            break
        
        message = data.split("#")[0] 
        s1 = int(data.split("#")[1]) 
        s2 = int(data.split("#")[2]) 

        print(f"Client: {message}")
    
        if verify_sig(s1, s2, message, pub_key):
            print(f"Server: Message '{message}' has not been tampered with. Signature has been verified.")
        else:
            print(f"Server: Message '{message}' has been tampered with. Signature was not verified succesfully.")

    conn.close()


if __name__ == "__main__":
    server()


