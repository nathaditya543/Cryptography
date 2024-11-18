import random
def is_prime(n, k=5):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    d = n - 1
    while d % 2 == 0:
        d //= 2
    for _ in range(k):
        if not miller_rabin_test(d, n):
            return False
    return True

def miller_rabin_test(d, n):
    a = 2 + random.randint(1, n - 4)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    while d != n - 1:
        x = (x * x) % n
        d *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False

def generate_large_prime(bits):
    while True:
        prime_candidate = random.getrandbits(bits)
        if prime_candidate % 2 == 0:
            continue
        if is_prime(prime_candidate):
            return prime_candidate

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x1, y1 = egcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return g, x, y

    g, x, y = egcd(e, phi)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % phi

def rsa_encrypt(message, e, n):
    message_as_int = int.from_bytes(message.encode('utf-8'), 'big')
    return pow(message_as_int, e, n)

def rsa_decrypt(ciphertext, d, n):
    decrypted_message_as_int = pow(ciphertext, d, n)
    decrypted_message = decrypted_message_as_int.to_bytes((decrypted_message_as_int.bit_length() + 7) // 8, 'big')
    return decrypted_message.decode('utf-8')

bits = 1024
p = generate_large_prime(bits)
q = generate_large_prime(bits)
n = p * q
phi_n = (p - 1) * (q - 1)
e = 65537
d = mod_inverse(e, phi_n)

message = "My name is Aditya Nath."

ciphertext = rsa_encrypt(message, e, n)

decrypted_message = rsa_decrypt(ciphertext, d, n)


print("p value:", p)
print("q value:", q)
print("n (p * q):", n)
print("phi(n):", phi_n)
print("e:", e)
print("d:", d)
print("Encrypted text:", ciphertext)
print("Decrypted text:", decrypted_message)
