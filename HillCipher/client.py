import socket

def send_request(operation, key, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    
    request = f"{operation}|{key}|{message}"
    client.send(request.encode())
    
    response = client.recv(4096).decode()
    client.close()
    return response

if __name__ == "__main__":
    operation = input("Enter operation (encrypt/decrypt): ").strip()
    key = input("Enter key : ").strip()
    message = input("Enter message: ").strip()
    
    result = send_request(operation, key, message)
    print(f"Result: {result}")
