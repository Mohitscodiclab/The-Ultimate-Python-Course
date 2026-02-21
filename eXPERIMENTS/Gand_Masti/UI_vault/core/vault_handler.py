import os
from core.crypto_utils import encrypt_file, decrypt_file

VAULT = "vault"

def ensure_vault():
    os.makedirs(VAULT, exist_ok=True)

def lock_vault(password):
    for f in os.listdir(VAULT):
        path = os.path.join(VAULT, f)
        if os.path.isfile(path) and not f.endswith(".lock"):
            encrypt_file(path, password)

def unlock_vault(password):
    for f in os.listdir(VAULT):
        path = os.path.join(VAULT, f)
        if f.endswith(".lock"):
            decrypt_file(path, password)