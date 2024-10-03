def aes():
    code = '''from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import numpy as np

# Complete S-box array (AES standard)
sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# Rcon (Round Constant) array
Rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

def key_expansion(key):
    # Initial key words (4 words of 4 bytes each)
    key_words = np.array(key).reshape(4, 4).T.tolist()

    for i in range(4, 44):
        temp = key_words[i-1]
        if i % 4 == 0:
            # RotWord and SubWord
            temp = [sbox[b] for b in temp[1:] + temp[:1]]
            # XOR with Rcon
            temp[0] ^= Rcon[i // 4 - 1]
        # XOR with word 4 positions earlier
        key_words.append([a ^ b for a, b in zip(key_words[i-4], temp)])
    
    # Flatten to get 176 bytes of expanded key
    expanded_key = [byte for word in key_words for byte in word]
    return expanded_key

def aes_encrypt(plaintext, key):
    # Key expansion to generate 176 bytes (11 rounds for AES-128)
    expanded_key = key_expansion(key)

    # Use the first 16 bytes of the expanded key for encryption
    cipher = AES.new(bytes(expanded_key[:16]), AES.MODE_ECB)
    padded_plaintext = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    
    return ciphertext

def aes_decrypt(ciphertext, key):
    # Key expansion to generate 176 bytes
    expanded_key = key_expansion(key)

    # Use the first 16 bytes of the expanded key for decryption
    cipher = AES.new(bytes(expanded_key[:16]), AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    return decrypted

# Example usage
plaintext = b'This is a secret message.'
key = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
       0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]

ciphertext = aes_encrypt(plaintext, key)
print("Ciphertext:", ciphertext.hex())

# Decryption (for verification)
decrypted = aes_decrypt(ciphertext, key)
print("Decrypted:", decrypted.decode())
    
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
from Crypto.Util.Padding import pad, unpad

# Permutation tables
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Number of shifts for each round
SHIFTS = [
    1, 1, 2, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 2, 2, 2, 1
]

def permute(bits, table):
    return [bits[i - 1] for i in table]

def shift_left(bits, n):
    return bits[n:] + bits[:n]

def key_expansion(key):
    # Initial permutation using PC1
    key_bits = [int(b) for b in format(int.from_bytes(key, byteorder='big'), '064b')]
    permuted_key = permute(key_bits, PC1)
    C, D = permuted_key[:28], permuted_key[28:]

    round_keys = []
    for shift in SHIFTS:
        # Shift C and D
        C = shift_left(C, shift)
        D = shift_left(D, shift)
        # Combine and permute using PC2
        round_key = permute(C + D, PC2)
        round_keys.append(round_key)

    # Convert each round key from bits to bytes
    return [int(''.join(map(str, round_key)), 2).to_bytes(6, byteorder='big') for round_key in round_keys]

def des_encrypt(plaintext, key):
    # Key expansion to generate 16 round keys
    round_keys = key_expansion(key)

    # Use PyCryptodome DES for encryption (with the initial 8-byte key)
    cipher = DES.new(key, DES.MODE_ECB)
    padded_plaintext = pad(plaintext, DES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    
    return ciphertext

def des_decrypt(ciphertext, key):
    # Key expansion to generate 16 round keys (not needed for library-based decryption)
    # Use PyCryptodome DES for decryption (with the initial 8-byte key)
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(ciphertext), DES.block_size)
    
    return decrypted

# Example usage
plaintext = b'This is a secret message.'
key = b'12345678'  # 8 bytes key for DES

ciphertext = des_encrypt(plaintext, key)
print("Ciphertext:", ciphertext.hex())

# Decryption (for verification)
decrypted = des_decrypt(ciphertext, key)
print("Decrypted:", decrypted.decode())


    
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