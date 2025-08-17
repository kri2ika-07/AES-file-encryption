from cryptography.fernet import Fernet
key= Fernet.generate_key()
with open ("mykey.key", "wb") as key_file:
    key_file.write (key)

print ("AES key generated and served as 'mykey.key' ") 