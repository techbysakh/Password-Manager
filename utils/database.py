# utils/database.py
import json
import os
from cryptography.fernet import Fernet

DATA_FILE = "vault.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def encrypt_data(data, fernet):
    encrypted = {}
    for site, accounts in data.items():
        encrypted[site] = {}
        for username, password in accounts.items():
            encrypted[site][username] = fernet.encrypt(password.encode()).decode()
    return encrypted

def decrypt_data(data, fernet):
    decrypted = {}
    for site, accounts in data.items():
        decrypted[site] = {}
        for username, encrypted_password in accounts.items():
            decrypted[site][username] = fernet.decrypt(encrypted_password.encode()).decode()
    return decrypted

def reset_passwords():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
