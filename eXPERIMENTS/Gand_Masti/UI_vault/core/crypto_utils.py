import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

def derive_key(password, salt):
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())

def encrypt_file(path, password):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    aes = AESGCM(key)
    nonce = os.urandom(12)

    data = open(path, "rb").read()
    encrypted = aes.encrypt(nonce, data, None)

    open(path + ".lock", "wb").write(salt + nonce + encrypted)
    os.remove(path)

def decrypt_file(path, password):
    data = open(path, "rb").read()

    salt = data[:16]
    nonce = data[16:28]
    content = data[28:]

    key = derive_key(password, salt)
    aes = AESGCM(key)
    decrypted = aes.decrypt(nonce, content, None)

    original = path.replace(".lock", "")
    open(original, "wb").write(decrypted)
    os.remove(path)