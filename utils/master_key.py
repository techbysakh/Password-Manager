import os
import hashlib
import base64
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

SALT_FILE = "salt.bin"
ITERATIONS = 100_000

backend = default_backend()

def generate_salt():
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt

def get_salt():
    if not os.path.exists(SALT_FILE):
        return generate_salt()
    with open(SALT_FILE, "rb") as f:
        return f.read()

def derive_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # Use SHA256 from the correct module
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def setup_master_key():
    print("🔑 First time setup: Create your master password")
    while True:
        pw1 = getpass.getpass("Enter new master password: ")
        pw2 = getpass.getpass("Confirm master password: ")
        if pw1 == pw2:
            salt = generate_salt()
            key = derive_key(pw1, salt)
            print("✅ Master password set.")
            return key, pw1
        else:
            print("❗ Passwords do not match. Try again.")

def get_derived_key():
    salt = get_salt()
    password = getpass.getpass("Enter master password: ")
    key = derive_key(password, salt)
    return key, password
