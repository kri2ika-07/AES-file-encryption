import os
from cryptography.fernet import Fernet

# load the key
with open ("mykey.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# get encrypted file
file_to_decrypt = input ("Enter the encrypted file name (with .enc):")

if not os.path.exists (file_to_decrypt):
    print ("File not found.")
    exit()

# decrypt
with open (file_to_decrypt, "rb") as enc_file:
    encrypted_data = enc_file.read()

try:
    decrypted_data = fernet.decrypt (encrypted_data)
except Exception as e:
    print ("Decryption failed:", str(e))
    exit()

# save decrypted file
original_name = file_to_decrypt.replace (".enc", "_decrypted")
with open(original_name, "wb") as dec_file:
    dec_file.write(decrypted_data)

print(f"Decrypted file saved as: {original_name}")