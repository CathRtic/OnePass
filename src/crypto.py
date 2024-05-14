import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode, b64decode

def encrypt_data(data, password, iterations=100000):
    try:
        salt = os.urandom(16)
        key = PBKDF2(password, salt, dkLen=32, count=iterations)
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return b64encode(salt + cipher.nonce + tag + ciphertext).decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

def decrypt_data(encrypted_data, password, iterations=100000):
    try:
        encrypted_data = b64decode(encrypted_data)
        salt, nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:48], encrypted_data[48:]
        key = PBKDF2(password, salt, dkLen=32, count=iterations)
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_data.decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return None
