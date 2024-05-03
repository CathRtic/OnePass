import customtkinter as ctk
import pyperclip
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode, b64decode

def encrypt_data(data, password):
    salt = b'YourSaltHere'
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_data(encrypted_data, password):
    encrypted_data = b64decode(encrypted_data)
    nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
    salt = b'YourSaltHere'
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode()

def load_passwords(master_password):
    try:
        with open('passwords.enc', 'r') as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, master_password)
        return dict(line.split('|') for line in data.strip().split('\n'))
    except FileNotFoundError:
        return {}

def save_passwords(data, master_password):
    plain_data = '\n'.join(f"{k}|{v}" for k, v in data.items())
    encrypted_data = encrypt_data(plain_data, master_password)
    with open('passwords.enc', 'w') as f:
        f.write(encrypted_data)

def refresh_list():
    global master_password
    passwords = load_passwords(master_password)
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    for service in passwords:
        service_button = ctk.CTkButton(scrollable_frame, text=service,
                                       command=lambda svc=service: password_action(svc))
        service_button.pack(pady=2, padx=10, fill=ctk.X)

def add_password():
    service = service_entry.get()
    password = password_entry.get()
    if service and password:
        passwords = load_passwords(master_password)
        passwords[service] = password
        save_passwords(passwords, master_password)
        refresh_list()
        service_entry.delete(0, END)
        password_entry.delete(0, END)
        ctk.CTkToplevel.show_info("Success", "Password added successfully!")

def show_temporary_message(message, duration=2000):  # duration in milliseconds
    message_label = ctk.CTkLabel(root, text=message, fg_color=("white", "gray38"))
    message_label.pack(pady=10)
    message_label.after(duration, message_label.destroy)


def password_action(service):
    passwords = load_passwords(master_password)
    password = passwords.get(service)
    if password:
        pyperclip.copy(password)
        show_temporary_message(f"Password for {service} copied to clipboard!")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("400x500")
root.title("Password Manager")

dialog = ctk.CTkInputDialog(title="Password Manager", text="Enter your master password:")
master_password = dialog.get_input()  # This will wait for the user to input and press OK or Cancel

scrollable_frame = ctk.CTkScrollableFrame(root)
scrollable_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

service_entry = ctk.CTkEntry(root, placeholder_text="Service Name")
service_entry.pack(fill=ctk.X, padx=20, pady=10)

password_entry = ctk.CTkEntry(root, placeholder_text="Password")
password_entry.pack(fill=ctk.X, padx=20, pady=10)

add_button = ctk.CTkButton(root, text="Add Password", command=add_password)
add_button.pack(fill=ctk.X, padx=20, pady=2)

refresh_list()

root.mainloop()
