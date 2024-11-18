import socket
import numpy as np
from PIL import Image
import math

# Define the character set
charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .'

# Map each character to an index
char_to_index = {char: idx for idx, char in enumerate(charset)}

# Function to map index to RGB value
def index_to_rgb(indices, rgb_muls, rgb_steps):
    rgb_values = [];
    ctr = 0
    for i in indices:
        r = i^rgb_muls[(0 + ctr) % 3] + 0
        g = i^rgb_muls[(1 + ctr) % 3] + 0
        b = i^rgb_muls[(2 + ctr) % 3] + 0
        rgb_muls[0] += rgb_steps[0]
        rgb_muls[1] += rgb_steps[1]
        rgb_muls[2] += rgb_steps[2]

        rgb_values.append((r,g,b))
        ctr += 1
    return rgb_values

# Function to encrypt text message into an image
def encrypt_text_to_image(text, rgb_muls, rgb_steps):
    message_length = len(text)
    dimension = math.ceil(math.sqrt(message_length))
    total_pixels = dimension * dimension
    
    # Pad the message if necessary
    padding_length = total_pixels - message_length
    padded_text = text + ' ' * padding_length  # Using x as the padding character

    # Convert the padded text to RGB values
    indices = []
    for i in padded_text:
        indices.append(char_to_index[i])
    rgb_values = index_to_rgb(indices, rgb_muls, rgb_steps)

    rgb_array = np.array(rgb_values, dtype=np.uint8).reshape((dimension, dimension, 3))
    image = Image.fromarray(rgb_array, 'RGB')
    scale_factor = 100
    # image2 = image.resize((dimension * scale_factor, dimension * scale_factor), Image.NEAREST)
    # image2.show()
    return image

def decrypt(img, rgb_muls, rgb_steps):
    arr = np.array(img)
    ctr = 0
    message = ""
    for j in arr:
        for i in j:
            r = i[0]^rgb_muls[(0 + ctr) % 3] + 0
            g = i[1]^rgb_muls[(1 + ctr) % 3] + 0
            b = i[2]^rgb_muls[(2 + ctr) % 3] + 0
            rgb_muls[0] += rgb_steps[0]
            rgb_muls[1] += rgb_steps[1]
            rgb_muls[2] += rgb_steps[2]
            ctr += 1
            if(r != b or r != g or b != g):
                print("error!")
            else:
                message += charset[r];

    return message


def server():
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host, port))  
    server_socket.listen(2)
    conn, address = server_socket.accept()  
    key = "642049533"
    scale_factor = 100

    print("Connection from: " + str(address))
    while True:  
        data = conn.recv(1024).decode()
        im2 = Image.open('encrypted_image.png')
        im2 = im2.resize((im2.size[0] * scale_factor, im2.size[1] * scale_factor), Image.NEAREST)
        im2.save('scaled_img.png')

        rgb_muls = [int(key[0:2]), int(key[2:4]), int(key[4:6])];
        rgb_steps = [int(key[6]), int(key[7]), int(key[8])];
        dec_image = Image.open('encrypted_image.png')
        print("Client: " + decrypt(dec_image, rgb_muls, rgb_steps)) 

        data = input('Server: ')
        rgb_muls = [int(key[0:2]), int(key[2:4]), int(key[4:6])];
        rgb_steps = [int(key[6]), int(key[7]), int(key[8])];
        image = encrypt_text_to_image(data, rgb_muls, rgb_steps)
        image.save('encrypted_image.png')
        conn.send(b"ack")  

    conn.close() 

if __name__ == '__main__':
    server()