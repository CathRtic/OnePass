import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode, b64decode

def encrypt_data(data, password):
    salt = os.urandom(16)  # Generate a random salt
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return b64encode(salt + cipher.nonce + tag + ciphertext).decode()

def decrypt_data(encrypted_data, password):
    encrypted_data = b64decode(encrypted_data)
    salt, nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:48], encrypted_data[48:]
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode()

def load_passwords(master_password):
    try:
        with open('passwords.enc', 'r') as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, master_password)
        return dict(line.split('|') for line in data.strip().split('\n'))
    except FileNotFoundError:
        return {}

def save_passwords(data, master_password):
    plain_data = '\n'.join(f"{k}|{v}" for k, v in data.items())
    encrypted_data = encrypt_data(plain_data, master_password)
    with open('passwords.enc', 'w') as f:
        f.write(encrypted_data)