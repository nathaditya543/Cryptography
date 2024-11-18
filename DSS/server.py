import socket
import hashlib

# Simple function to hash the message
def hash_message(message):
    return hashlib.sha256(message.encode()).hexdigest()

# Function to verify the signature
def verify_message(message, signature, private_key):
    # Create the expected signature by hashing the received message and appending the private key
    expected_signature = hash_message(message) + private_key
    return signature == expected_signature

def server():
    private_key = "my_private_key"  # Simulating a known private key for verification

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 12345))
        s.listen()
        print("Server listening for connections...")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            # Receive the message
            full_message = conn.recv(1024).decode()
            message = full_message[:full_message.index("#")]
            signature = full_message[full_message.index("#")+1:]

            # Verify the message
            if verify_message(message, signature, private_key):
                print("Message is valid!")
            else:
                print("Message is invalid or has been tampered with.")

server()
