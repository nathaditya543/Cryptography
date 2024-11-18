import socket

def send_request(command, text, key, host='127.0.0.1', port=65432):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    request = f'{command};{text};{key}'
    client.send(request.encode())

    response = client.recv(1024).decode()
    print("Response from server:", response)

    client.close()

if __name__ == '__main__':
    while True:
        command = input("Enter command (ENCRYPT/DECRYPT or EXIT to quit): ").strip().upper()
        if command == 'EXIT':
            break
        elif command not in ['ENCRYPT', 'DECRYPT']:
            print("Invalid command. Please enter ENCRYPT or DECRYPT.")
            continue
        
        text = input("Enter the text: ").strip().upper()
        key = input("Enter the key: ").strip().upper()

        send_request(command, text, key)
