def aes():
    code = '''from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

key = get_random_bytes(16)
iv = get_random_bytes(16)

def aes_encrypt(plain_text):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
    return cipher_text

def aes_decrypt(cipher_text):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_text = unpad(cipher.decrypt(cipher_text), AES.block_size).decode('utf-8')
    return plain_text

plain_text = input("Enter a Plaintext: ")
print("Original Message:", plain_text)
cipher_text = aes_encrypt(plain_text)
print("Encrypted Message (in bytes):", cipher_text)
decrypted_text = aes_decrypt(cipher_text)
print("Decrypted Message:", decrypted_text)

    
    '''
    print(code)


def caesar():
    code = '''def caesar_cipher_encrypt(plaintext, shift):
    cipher_text = ''
    for i in range(len(plaintext)):
        char = plaintext[i]

        if char.isupper():
            cipher_text += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            cipher_text += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            cipher_text += char
    return cipher_text

def caesar_cipher_decrypt(ciphertext, shift):
    plaintext = ''
    for i in range(len(ciphertext)):
        char = ciphertext[i]

        if char.isupper():
            plaintext += chr((ord(char) - shift - 65) % 26 + 65)
        elif char.islower():
            plaintext += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            plaintext += char
    return plaintext

# Input from the user
plaintext = input("Enter the Plaintext: ")
shift = int(input("Enter the shift value: "))

# Encryption
ciphertext = caesar_cipher_encrypt(plaintext, shift)
print("Cipher Text = " + ciphertext)

# Decryption
decrypted_text = caesar_cipher_decrypt(ciphertext, shift)
print("Decrypted Text = " + decrypted_text)

    
    '''
    print(code)




def des():
    code = '''from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import binascii

def pad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text

def encrypt_DES(key, message):
    des = DES.new(key, DES.MODE_ECB)
    padded_message = pad(message)
    encrypted_message = des.encrypt(padded_message.encode('utf-8'))
    return binascii.hexlify(encrypted_message).decode('utf-8')

def decrypt_DES(key, encrypted_message):
    des = DES.new(key, DES.MODE_ECB)
    decrypted_message = des.decrypt(binascii.unhexlify(encrypted_message))
    return decrypted_message.decode('utf-8').rstrip()

key = get_random_bytes(8)
message = input("Enter a Message: ")
print(f"Original Message: {message}")
encrypted_message = encrypt_DES(key, message)
print(f"Encrypted Message (Hex): {encrypted_message}")
decrypted_message = decrypt_DES(key, encrypted_message)
print(f"Decrypted Message: {decrypted_message}")



    
    '''
    print(code)






def diffie():
    code = '''def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def is_primitive_root(alpha, q):
    required_set = set(range(1, q))  # Set of integers from 1 to q-1
    return set(pow(alpha, power, q) for power in range(1, q)) == required_set

def find_primitive_root(q):
    if not is_prime(q):
        raise ValueError(f"{q} is not a prime number, primitive root does not exist.")
    for alpha in range(2, q):
        if is_primitive_root(alpha, q):
            return alpha
    return None

def diffie_hellman(prime_q, primitive_root, private_a, private_b):
    public_a = pow(primitive_root, private_a, prime_q)
    public_b = pow(primitive_root, private_b, prime_q)
    shared_secret_a = pow(public_b, private_a, prime_q)
    shared_secret_b = pow(public_a, private_b, prime_q)
    return public_a, public_b, shared_secret_a, shared_secret_b

q = int(input("Enter the a Large Prime 'q': "))
alpha = find_primitive_root(q)
x_A = int(input("Enter the a Private key of A': "))
x_B = int(input("Enter the a Private key of B': "))

if x_A >= q or x_B >= q:
    raise ValueError(f"Private keys must be less than {q}")
public_a, public_b, shared_secret_a, shared_secret_b = diffie_hellman(q, alpha, x_A, x_B)

print("Alpha: ", alpha)
print("y_A (Public key of A): ", public_a)
print("y_B (Public key of B): ", public_b)
print(f"Shared Secret computed by A: {shared_secret_a}")
print(f"Shared Secret computed by B: {shared_secret_b}")

if shared_secret_a == shared_secret_b:
    print("Key Exchange successful! Shared Secret is the Same.")
else:
    print("Key Exchange Failed!")


    
    '''
    print(code)





def hill():
    code = '''def createMatrix(size):
    return [[0] * size for _ in range(size)]

def getKeyMatrix(key, size, keyMatrix):
    k = 0
    for i in range(size):
        for j in range(size):
            keyMatrix[i][j] = ord(key[k]) % 65
            k += 1

def encrypt(messageVector, keyMatrix, size, cipherMatrix):
    for i in range(size):
        for j in range(1):
            cipherMatrix[i][j] = 0
            for x in range(size):
                cipherMatrix[i][j] += (keyMatrix[i][x] * messageVector[x][j])
            cipherMatrix[i][j] = cipherMatrix[i][j] % 26

def HillCipher(message, key, size):
    keyMatrix = createMatrix(size)
    messageVector = [[0] for _ in range(size)]
    cipherMatrix = [[0] for _ in range(size)]
    getKeyMatrix(key, size, keyMatrix)
    for i in range(size):
        messageVector[i][0] = ord(message[i]) % 65
    encrypt(messageVector, keyMatrix, size, cipherMatrix)
    CipherText = []
    for i in range(size):
        CipherText.append(chr(cipherMatrix[i][0] + 65))
    print("Ciphertext: ", "".join(CipherText))

size = int(input("Enter the size of the matrix (e.g., 3 for 3x3): "))
message = input(f"Enter the {size}-letter Plaintext: ").upper()
key = input(f"Enter the {size*size}-letter key: ").upper()
HillCipher(message, key, size)


    
    '''
    print(code)






def playfair():
    code = '''def create_matrix(keyword):
    keyword = ''.join(sorted(set(keyword), key=keyword.index))
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    matrix = [c for c in keyword if c in alphabet]
    
    for char in alphabet:
        if char not in matrix:
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def preprocess_text(text):
    text = text.upper().replace('J', 'I')
    digraphs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            digraphs.append(a + 'X')
            i += 1
        else:
            digraphs.append(a + b)
            i += 2
    return digraphs

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None

def encrypt_digraph(digraph, matrix):
    r1, c1 = find_position(matrix, digraph[0])
    r2, c2 = find_position(matrix, digraph[1])
    
    if r1 == r2:
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    elif c1 == c2:
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]

def decrypt_digraph(digraph, matrix):
    r1, c1 = find_position(matrix, digraph[0])
    r2, c2 = find_position(matrix, digraph[1])
    if r1 == r2:
        return matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
    elif c1 == c2:
        return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]

def playfair_cipher(text, keyword, mode='encrypt'):
    matrix = create_matrix(keyword)
    digraphs = preprocess_text(text)
    if mode == 'encrypt':
        return ''.join(encrypt_digraph(d, matrix) for d in digraphs)
    elif mode == 'decrypt':
        return ''.join(decrypt_digraph(d, matrix) for d in digraphs)

keyword = input("Enter the keyword: ").upper().replace('J', 'I')
plaintext = input("Enter the plaintext to encrypt: ").upper()

encrypted = playfair_cipher(plaintext, keyword, mode='encrypt')
print("Encrypted:", encrypted)

decrypted = playfair_cipher(encrypted, keyword, mode='decrypt')
print("Decrypted:", decrypted)


    
    '''
    print(code)








def rail():
    code = '''def encrypt_rail_fence(text, key):
    rail = [['\n' for i in range(len(text))] for j in range(key)]
    direction_down = False
    row, col = 0, 0
    
    for i in range(len(text)):
        rail[row][col] = text[i]
        col += 1
        
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1
    
    ciphertext = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                ciphertext.append(rail[i][j])
    
    return "".join(ciphertext)

def decrypt_rail_fence(cipher, key):
    rail = [['\n' for i in range(len(cipher))] for j in range(key)]
    direction_down = None
    row, col = 0, 0
    
    for i in range(len(cipher)):
        if row == 0:
            direction_down = True
        if row == key - 1:
            direction_down = False
        
        rail[row][col] = '*'
        col += 1
        row += 1 if direction_down else -1
    
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1
    
    plaintext = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            direction_down = True
        if row == key - 1:
            direction_down = False
        
        if rail[row][col] != '*':
            plaintext.append(rail[row][col])
            col += 1
        row += 1 if direction_down else -1
    
    return "".join(plaintext)

plaintext = input("Enter the plaintext: ")
key = int(input("Enter the key (number of rails): "))

ciphertext = encrypt_rail_fence(plaintext, key)
print(f"Ciphertext: {ciphertext}")

decrypted_text = decrypt_rail_fence(ciphertext, key)
print(f"Decrypted Text: {decrypted_text}")

    
    '''
    print(code)







def rsa():
    code = '''import math

def gcd(a, h):
    temp = 0
    while(1):
        temp = a % h
        if (temp == 0):
            return h
        a = h
        h = temp

p = int(input("Enter a prime number p: "))
q = int(input("Enter another prime number q: "))
n = p * q
e = 2
phi = (p - 1) * (q - 1)

while (e < phi):
    if gcd(e, phi) == 1:
        break
    else:
        e = e + 1

k = 2
d = (1 + (k * phi)) // e

msg = int(input("Enter a message to encrypt (as an integer): "))
print("Message data = ", msg)

c = pow(msg, e) % n
print("Encrypted data = ", c)

m = pow(c, d) % n
print("Original Message Sent = ", m)


    
    '''
    print(code)






def vigenere():
    code = '''def generate_key(msg, key):
    key = list(key)
    if len(msg) == len(key):
        return key
    else:
        for i in range(len(msg) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def encrypt_vigenere(msg, key):
    encrypted_text = []
    key = generate_key(msg, key)
    for i in range(len(msg)):
        char = msg[i]
        if char.isupper():
            encrypted_char = chr((ord(char) + ord(key[i]) - 2 * ord('A')) % 26 + ord('A'))
        elif char.islower():
            encrypted_char = chr((ord(char) + ord(key[i]) - 2 * ord('a')) % 26 + ord('a'))
        else:
            encrypted_char = char
        encrypted_text.append(encrypted_char)
    return "".join(encrypted_text)

def decrypt_vigenere(msg, key):
    decrypted_text = []
    key = generate_key(msg, key)
    for i in range(len(msg)):
        char = msg[i]
        if char.isupper():
            decrypted_char = chr((ord(char) - ord(key[i]) + 26) % 26 + ord('A'))
        elif char.islower():
            decrypted_char = chr((ord(char) - ord(key[i]) + 26) % 26 + ord('a'))
        else:
            decrypted_char = char
        decrypted_text.append(decrypted_char)
    return "".join(decrypted_text)

text_to_encrypt = input("Enter the Plaintext to encrypt: ")
key = input("Enter the encryption key: ")
encrypted_text = encrypt_vigenere(text_to_encrypt, key)
print(f"Encrypted Text: {encrypted_text}")
decrypted_text = decrypt_vigenere(encrypted_text, key)
print(f"Decrypted Text: {decrypted_text}")

    
    '''
    print(code)