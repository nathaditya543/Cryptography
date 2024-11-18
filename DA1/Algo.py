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
        print(i, rgb_muls[(0 + ctr) % 3], r)
        print(i, rgb_muls[(1 + ctr) % 3], g)
        print(i, rgb_muls[(2 + ctr) % 3], b)
        
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
    print(indices)

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

if __name__ == "__main__":
    # Example text message
    message = "Cryptography"
    key = "642049533"
    rgb_muls = [int(key[0:2]), int(key[2:4]), int(key[4:6])];
    rgb_steps = [int(key[6]), int(key[7]), int(key[8])];

    # Encrypt the message into a perfect square image
    image = encrypt_text_to_image(message, rgb_muls, rgb_steps)
    image.save('encrypted_image.png')
    
    rgb_muls = [int(key[0:2]), int(key[2:4]), int(key[4:6])];
    rgb_steps = [int(key[6]), int(key[7]), int(key[8])];
    dec_image = Image.open('encrypted_image.png')
    print(decrypt(dec_image, rgb_muls, rgb_steps))
