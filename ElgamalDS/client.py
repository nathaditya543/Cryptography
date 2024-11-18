import socket
import hashlib

def keygen(p,alpha,x):
    y = pow(alpha,x) % p
    return (p, alpha, y)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def calc_sig_pair(data, pub_key, x):
    p = pub_key[0]
    alpha = pub_key[1]
    y = pub_key[2]
    k = 23
    hash_object = hashlib.sha256(data.encode())
    m = int(hash_object.hexdigest(), 16)%p
    kinv = modinv(k,p-1)

    s1 = pow(alpha,k)%p
    s2 = (kinv*(m-x*s1))%(p-1)
    return(s1,s2)


def client(priv_key):
    client_socket = socket.socket()
    host = '127.0.0.1'
    port = 5000

    client_socket.connect((host, port))
    data = ''
    
    delim = "#"
    pub_str = str(pub_key[0]) + delim + str(pub_key[1]) + delim + str(pub_key[2]) 
    client_socket.send(pub_str.encode())
    

    while(True):
        data = input("Client: ")
        if(data == "exit"):
            break

        sig_pair = calc_sig_pair(data, pub_key, priv_key)

        choice = input("Do you want to tamper the message before sending it ? (y/n): ")
        if(choice == 'y'):
            data = input("Enter tampered Message: ")

        message = data + delim + str(sig_pair[0]) + delim +  str(sig_pair[1])
        client_socket.send(message.encode())

    
    client_socket.close()


if __name__ == "__main__":
    p = 997
    alpha = 2
    priv_key = 5
    pub_key = keygen(p,alpha,priv_key)
    client(priv_key)