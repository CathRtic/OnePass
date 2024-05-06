import pyperclip
from password_generator import generate_password
from crypto import load_passwords, save_passwords
import customtkinter as ctk
from tkinter import *


def refresh_list(scrollable_frame, master_password, root):
    passwords = load_passwords(master_password)
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    for service in passwords:
        service_button = ctk.CTkButton(scrollable_frame, text=service,
                                       command=lambda svc=service: password_action(svc, master_password, root))
        service_button.pack(pady=2, padx=10, fill=ctk.X)

def add_password(service_entry, password_entry, master_password, scrollable_frame, root):
    service = service_entry.get()
    password = password_entry.get()
    if service and password:
        passwords = load_passwords(master_password)
        passwords[service] = password
        save_passwords(passwords, master_password)
        refresh_list(scrollable_frame, master_password, root)
        service_entry.delete(0, END)
        password_entry.delete(0, END)
        show_temporary_message(root, "Password added successfully!")


def password_action(service, master_password, root):
    passwords = load_passwords(master_password)
    password = passwords.get(service)
    if password:
        pyperclip.copy(password)
        show_temporary_message(root, f"Password for {service} copied to clipboard!")

def generate_and_display_password(password_entry):
    length = int(ctk.CTkInputDialog(title="Password Generator", text="Enter Password Length:").get_input())
    password = generate_password(length)
    password_entry.delete(0, END)  # Clear the entry widget first
    password_entry.insert(0, password)  # Insert the generated password

def show_temporary_message(root, message, duration=1400):
    message_label = ctk.CTkLabel(root, text=message, fg_color=("white", "gray38"))
    message_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
    message_label.after(duration, message_label.destroy)


