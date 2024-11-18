import socket
import hashlib

# Simple function to hash the message
def hash_message(message):
    return hashlib.sha256(message.encode()).hexdigest()

# Function to "sign" the message
def sign_message(message, private_key):
    # Create the "signature" by hashing the message and appending the private key
    return hash_message(message) + private_key

# Function to get user input and sign the message
def client():
    private_key = "my_private_key"  # Simulating a private key

    # User input for the message
    message = input("Enter a message to send: ")
    signature = sign_message(message, private_key)
    message += "#"

    # Ask user if they want to modify the message
    choice = input("Do you want to modify the message? (yes/no): ").strip().lower()

    if choice == 'yes':
        message = input("Enter the new message: ")
        message += "#"

    # Send the message and signature to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12345))
        s.send(message.encode())  # Send message
        s.send(signature.encode())  # Send signature

    print("Message and signature sent to the server.")
    print(message)
    print(signature)

client()
