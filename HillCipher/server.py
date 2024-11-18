import socket

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def create_matrix_of_integers_from_string(string, size):
    integers = [ord(char) - ord('A') for char in string]
    matrix = [integers[i:i+size] for i in range(0, len(integers), size)]
    return matrix

def matrix_multiply(A, B):
    product = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                product[i][j] += A[i][k] * B[k][j]
    return product

def hill_encrypt(plaintext, key):
    size = int(len(key) ** 0.5)
    key_matrix = create_matrix_of_integers_from_string(key, size)
    plaintext_vector = [ord(char) - ord('A') for char in plaintext]
    plaintext_matrix = [plaintext_vector[i:i+size] for i in range(0, len(plaintext_vector), size)]
    
    ciphertext_matrix = matrix_multiply(plaintext_matrix, key_matrix)
    ciphertext_matrix = [[num % 26 for num in row] for row in ciphertext_matrix]
    ciphertext = ''.join([chr(num + ord('A')) for row in ciphertext_matrix for num in row])
    return ciphertext

def hill_decrypt(ciphertext, key):
    size = int(len(key) ** 0.5)
    key_matrix = create_matrix_of_integers_from_string(key, size)
    
    determinant = (key_matrix[0][0] * (key_matrix[1][1] * key_matrix[2][2] - key_matrix[1][2] * key_matrix[2][1])
                - key_matrix[0][1] * (key_matrix[1][0] * key_matrix[2][2] - key_matrix[1][2] * key_matrix[2][0])
                + key_matrix[0][2] * (key_matrix[1][0] * key_matrix[2][1] - key_matrix[1][1] * key_matrix[2][0])) % 26

    determinant_inv = mod_inverse(determinant, 26)
    
    if determinant_inv is None:
        return "Invalid key, cannot decrypt"
    
    adjugate = [
        [(key_matrix[1][1] * key_matrix[2][2] - key_matrix[1][2] * key_matrix[2][1]) % 26, 
         (key_matrix[0][2] * key_matrix[2][1] - key_matrix[0][1] * key_matrix[2][2]) % 26, 
         (key_matrix[0][1] * key_matrix[1][2] - key_matrix[0][2] * key_matrix[1][1]) % 26],
        [(key_matrix[1][2] * key_matrix[2][0] - key_matrix[1][0] * key_matrix[2][2]) % 26, 
         (key_matrix[0][0] * key_matrix[2][2] - key_matrix[0][2] * key_matrix[2][0]) % 26, 
         (key_matrix[0][2] * key_matrix[1][0] - key_matrix[0][0] * key_matrix[1][2]) % 26],
        [(key_matrix[1][0] * key_matrix[2][1] - key_matrix[1][1] * key_matrix[2][0]) % 26, 
         (key_matrix[0][1] * key_matrix[2][0] - key_matrix[0][0] * key_matrix[2][1]) % 26, 
         (key_matrix[0][0] * key_matrix[1][1] - key_matrix[0][1] * key_matrix[1][0]) % 26]
    ]
    
    inverse_key_matrix = [[(determinant_inv * adjugate[i][j]) % 26 for j in range(size)] for i in range(size)]
    
    ciphertext_vector = [ord(char) - ord('A') for char in ciphertext]
    ciphertext_matrix = [ciphertext_vector[i:i+size] for i in range(0, len(ciphertext_vector), size)]
    
    plaintext_matrix = matrix_multiply(ciphertext_matrix, inverse_key_matrix)
    plaintext_matrix = [[num % 26 for num in row] for row in plaintext_matrix]
    plaintext = ''.join([chr(num + ord('A')) for row in plaintext_matrix for num in row])
    return plaintext

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    operation, key, message = request.split('|')
    
    if operation == 'encrypt':
        response = hill_encrypt(message, key)
    elif operation == 'decrypt':
        response = hill_decrypt(message, key)
    else:
        response = "Invalid operation"
    
    client_socket.send(response.encode())
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
