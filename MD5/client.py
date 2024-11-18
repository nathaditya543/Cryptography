import socket
import binascii
def xor_encrypt_decrypt(message, key):
    encrypted_message = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, key * len(message)))
    return encrypted_message

def left_rotate(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

def md5_hash(message):

    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476

    message_bytes = bytearray(message, 'utf-8')
    original_len_bits = len(message_bytes) * 8
    message_bytes.append(0x80)  

    while (len(message_bytes) * 8) % 512 != 448:
        message_bytes.append(0)

    message_bytes += original_len_bits.to_bytes(8, byteorder='little')
    K = [i for i in range(64)]
    print("Processing message in blocks of 512 bits")

    for i in range(0, len(message_bytes), 64):
        block = message_bytes[i:i+64]
        M = [int.from_bytes(block[j:j+4], byteorder='little') for j in range(0, 64, 4)]
        print(f"Processing block {i // 64 + 1}: {M}")
        AA, BB, CC, DD = A, B, C, D
        for round_num in range(4):
            for j in range(round_num * 16, (round_num + 1) * 16):
                if 0 <= j <= 15:
                    F = (B & C) | (~B & D)
                    g = j
                elif 16 <= j <= 31:
                    F = (D & B) | (~D & C)
                    g = (5 * j + 1) % 16
                elif 32 <= j <= 47:
                    F = B ^ C ^ D
                    g = (3 * j + 5) % 16
                else:
                    F = C ^ (B | ~D)
                    g = (7 * j) % 16

                F = (F + A + K[j] + M[g]) & 0xFFFFFFFF
                A = D
                D = C
                C = B
                B = (B + left_rotate(F, 7)) & 0xFFFFFFFF


            print(f"Round {round_num + 1}: A={hex(A)} B={hex(B)} C={hex(C)} D={hex(D)}")


        A = (A + AA) & 0xFFFFFFFF
        B = (B + BB) & 0xFFFFFFFF
        C = (C + CC) & 0xFFFFFFFF
        D = (D + DD) & 0xFFFFFFFF


    hash_value = (A.to_bytes(4, 'little') + B.to_bytes(4, 'little') +
                  C.to_bytes(4, 'little') + D.to_bytes(4, 'little'))

    return hash_value.hex()


def client_program():
    client_socket = socket.socket()
    host = '127.0.0.1'
    port = 5000

    client_socket.connect((host, port))
    data = ''
    key = "mysecretkey" 
    while(data.lower().strip() != "exit"):
        data = input("\n\nClient: ")
        encrypted_message = xor_encrypt_decrypt(data, key)

        print(f"Encrypted message being sent: {binascii.hexlify(encrypted_message.encode()).decode()}")
        client_socket.send(encrypted_message.encode())

        encrypted_message = client_socket.recv(1024).decode()
        print(f"Received encrypted message: {binascii.hexlify(encrypted_message.encode()).decode()}")

        decrypted_message = xor_encrypt_decrypt(encrypted_message, key)
        print(f"Decrypted message: {decrypted_message}")

        mac = md5_hash(decrypted_message)
        print(f"Message Authentication Code (MAC): {mac}")
    
    client_socket.close()

if __name__ == "__main__":
    client_program()
