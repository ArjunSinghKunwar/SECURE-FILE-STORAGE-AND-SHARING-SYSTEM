from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

KEY_SIZE = 32  # 256-bit AES key
HMAC_KEY_SIZE = 32

def generate_keys():
    return os.urandom(KEY_SIZE), os.urandom(HMAC_KEY_SIZE)

def encrypt_file(data, aes_key, hmac_key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    # pad data to 16 bytes
    padding_len = 16 - (len(data) % 16)
    data += bytes([padding_len]) * padding_len
    ciphertext = encryptor.update(data) + encryptor.finalize()
    h = hmac.HMAC(hmac_key, hashes.SHA256())
    h.update(iv + ciphertext)
    tag = h.finalize()
    return iv + ciphertext + tag

def decrypt_file(encrypted, aes_key, hmac_key):
    iv = encrypted[:16]
    tag = encrypted[-32:]
    ciphertext = encrypted[16:-32]
    h = hmac.HMAC(hmac_key, hashes.SHA256())
    h.update(iv + ciphertext)
    h.verify(tag)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    padding_len = padded[-1]
    return padded[:-padding_len]