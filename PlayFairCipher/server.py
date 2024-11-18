import socket
import threading

def generate_key_table(key):
    key = key.upper().replace('J', 'I')
    key_table = []
    used_chars = set()

    for char in key:
        if char not in used_chars and char.isalpha():
            key_table.append(char)
            used_chars.add(char)

    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    for char in alphabet:
        if char not in used_chars:
            key_table.append(char)
            used_chars.add(char)

    return [key_table[i:i+5] for i in range(0, 25, 5)]

def preprocess_text(text):
    text = text.upper().replace('J', 'I')
    processed_text = ""
    i = 0

    while i < len(text):
        char1 = text[i]
        if not char1.isalpha():
            i += 1
            continue

        char2 = text[i + 1] if i + 1 < len(text) and text[i + 1].isalpha() else 'X'

        if char1 == char2:
            processed_text += char1 + 'X'
            i += 1
        else:
            processed_text += char1 + char2
            i += 2

    if len(processed_text) % 2 != 0:
        processed_text += 'X'

    return processed_text

def find_position(char, key_table):
    for row in range(5):
        for col in range(5):
            if key_table[row][col] == char:
                return row, col
    return None

def playfair_encrypt(text, key):
    key_table = generate_key_table(key)
    text = preprocess_text(text)
    encrypted_text = ""

    for i in range(0, len(text), 2):
        row1, col1 = find_position(text[i], key_table)
        row2, col2 = find_position(text[i + 1], key_table)

        if row1 is None or row2 is None:
            continue

        if row1 == row2:
            encrypted_text += key_table[row1][(col1 + 1) % 5] + key_table[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted_text += key_table[(row1 + 1) % 5][col1] + key_table[(row2 + 1) % 5][col2]
        else:
            encrypted_text += key_table[row1][col2] + key_table[row2][col1]

    return encrypted_text

def playfair_decrypt(text, key):
    key_table = generate_key_table(key)
    decrypted_text = ""

    for i in range(0, len(text), 2):
        row1, col1 = find_position(text[i], key_table)
        row2, col2 = find_position(text[i + 1], key_table)

        if row1 is None or row2 is None:
            continue

        if row1 == row2:
            decrypted_text += key_table[row1][(col1 - 1) % 5] + key_table[row2][(col2 - 1) % 5]
        elif col1 == col2:
            decrypted_text += key_table[(row1 - 1) % 5][col1] + key_table[(row2 - 1) % 5][col2]
        else:
            decrypted_text += key_table[row1][col2] + key_table[row2][col1]

    return decrypted_text

def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024).decode()

        if not request:
            break

        command, text, key = request.split(';')

        if command == 'ENCRYPT':
            response = playfair_encrypt(text, key)
        elif command == 'DECRYPT':
            response = playfair_decrypt(text, key)
        else:
            response = 'INVALID COMMAND'

        client_socket.send(response.encode())

    client_socket.close()

def start_server(host='127.0.0.1', port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f'Server listening on {host}:{port}')

    try:
        while True:
            client_socket, addr = server.accept()
            print(f'Accepted connection from {addr}')
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
        server.close()

if __name__ == '__main__':
    start_server()
