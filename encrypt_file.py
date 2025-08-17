import os
import json
from cryptography.fernet import Fernet
from datetime import datetime
import hashlib

def generate_hash(file_data):
    return hashlib.sha256 (file_data).hexdigest()

# Load key
with open("mykey.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# Function to generate file hash
def generate_hash(file_data):
    return hashlib.sha256(file_data).hexdigest()

# Get file to encrypt
file_to_encrypt = input("Enter the file name to encrypt (with extension): ")

if not os.path.exists(file_to_encrypt):
    print("File not found")
    exit()

# Encrypt file
with open(file_to_encrypt, "rb") as file:
    original_data = file.read()

encrypted_data = fernet.encrypt(original_data)

# Save encrypted file
os.makedirs("encrypted_files", exist_ok=True)
enc_file_path = f"encrypted_files/{file_to_encrypt}.enc"

with open(enc_file_path, "wb") as enc_file:
    enc_file.write(encrypted_data)

# Metadata
metadata = {
    "file_name": file_to_encrypt,
    "encrypted_file": enc_file_path,
    "timestamp": datetime.now().isoformat(),
    "hash": generate_hash(original_data)
}

with open("metadata.json", "w") as meta_file:
    json.dump(metadata, meta_file, indent=4)

print(" File encrypted and metadata saved.")
