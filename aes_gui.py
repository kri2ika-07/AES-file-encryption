import os
import json
import hashlib
from tkinter import Tk, Label, Button, filedialog, messagebox
from cryptography.fernet import Fernet
from datetime import datetime

# === Load Key ===
with open("mykey.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# === Generate Hash ===
def generate_hash(data):
    return hashlib.sha256(data).hexdigest()

# === Encrypt File ===
def encrypt_file(filepath):
    try:
        with open(filepath, "rb") as f:
            original_data = f.read()

        encrypted_data = fernet.encrypt(original_data)

        os.makedirs("encrypted_files", exist_ok=True)
        filename = os.path.basename(filepath)
        encrypted_path = f"encrypted_files/{filename}.enc"

        with open(encrypted_path, "wb") as f:
            f.write(encrypted_data)

        metadata = {
            "file_name": filename,
            "encrypted_file": encrypted_path,
            "timestamp": datetime.now().isoformat(),
            "hash": generate_hash(original_data)
        }

        with open("metadata.json", "w") as meta_file:
            json.dump(metadata, meta_file, indent=4)

        messagebox.showinfo("✅ Success", f"File encrypted and saved as:\n{encrypted_path}")

    except Exception as e:
        messagebox.showerror("❌ Error", str(e))

# === Decrypt File ===
def decrypt_file(filepath):
    try:
        with open(filepath, "rb") as enc_file:
            encrypted_data = enc_file.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        original_name = filepath.replace(".enc", "_decrypted")
        with open(original_name, "wb") as f:
            f.write(decrypted_data)

        messagebox.showinfo("✅ Success", f"File decrypted and saved as:\n{original_name}")

    except Exception as e:
        messagebox.showerror("❌ Error", f"Decryption failed:\n{str(e)}")

# === Button Callbacks ===
def select_and_encrypt():
    file_path = filedialog.askopenfilename()
    if file_path:
        encrypt_file(file_path)

def select_and_decrypt():
    file_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
    if file_path:
        decrypt_file(file_path)

# === GUI Setup ===
app = Tk()
app.title("🔐 AES File Encryptor")
app.geometry("350x200")
app.resizable(False, False)

Label(app, text="Secure File Storage System", font=("Helvetica", 14, "bold")).pack(pady=10)
Button(app, text="Encrypt a File", command=select_and_encrypt, width=25).pack(pady=10)
Button(app, text="Decrypt a File", command=select_and_decrypt, width=25).pack(pady=10)
Label(app, text="Made with Python 🐍", font=("Helvetica", 9)).pack(side="bottom", pady=10)

app.mainloop()
