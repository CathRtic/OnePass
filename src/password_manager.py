import pyperclip
from password_generator import generate_password
from crypto import *
import customtkinter as ctk
from tkinter import *
import tkinter.messagebox as messagebox
try:
    def load_passwords(master_password):
        try:
            with open('passwords.enc', 'r') as f:
                encrypted_data = f.read()
            data = decrypt_data(encrypted_data, master_password)
            # Create a dictionary, safely ignoring malformed lines
            return {k: v for k, v in (line.split('|', 1) for line in data.strip().split('\n') if '|' in line)}
        except FileNotFoundError:
            return {}


    def save_passwords(data, master_password):
        plain_data = '\n'.join(f"{k}|{v}" for k, v in data.items())
        encrypted_data = encrypt_data(plain_data, master_password)
        with open('passwords.enc', 'w') as f:
            f.write(encrypted_data)

    def refresh_list(scrollable_frame, master_password, root):
        passwords = load_passwords(master_password)
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        for service in passwords:
            row_frame = ctk.CTkFrame(scrollable_frame)
            row_frame.pack(pady=2, padx=10, fill=ctk.X)

            service_button = ctk.CTkButton(row_frame, text=service,
                                        command=lambda svc=service: password_action(svc, master_password, root))
            service_button.pack(side='left', expand=True, fill=ctk.X, padx = 5)

            delete_button = ctk.CTkButton(row_frame, text='X', width = 5, fg_color = '#bd1919',
                                        command=lambda svc=service: delete_password_action(svc, master_password, scrollable_frame, root))
            delete_button.pack(side='right')

    def add_password(service_entry, password_entry, master_password, scrollable_frame, root):
        service = service_entry.get().strip()
        password = password_entry.get().strip()
        if not service or not password:
            show_temporary_message(root, "Please enter Service Name and Password")
            return
        passwords = load_passwords(master_password)
        passwords[service] = password
        save_passwords(passwords, master_password)
        service_entry.delete(0, END)
        password_entry.delete(0, END)
        refresh_list(scrollable_frame, master_password, root)
        show_temporary_message(root, "Password added successfully!")



    def password_action(service, master_password, root):
        passwords = load_passwords(master_password)
        password = passwords.get(service)
        if password:
            pyperclip.copy(password)
            show_temporary_message(root, f"Password for {service} copied to clipboard!")

    def generate_and_display_password(password_entry, root):
        length_str = ctk.CTkInputDialog(title="Password Generator", text="Enter Password Length:").get_input()
        if not length_str.isdigit():
            error = ctk.CTkToplevel(root)
            error.title("Invalid")
            error.geometry("210x100")

            label = ctk.CTkLabel(error, text="Invalid: Please input a number", fg_color="transparent")
            label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            return
        length = int(length_str)
        password = generate_password(length)
        password_entry.configure(show='')  # Temporarily remove the show attribute
        password_entry.delete(0, END)  # Clear the entry widget
        password_entry.insert(0, password)  # Insert the generated password
        password_entry.configure(show='*')  # Reapply the show attribute

    def show_temporary_message(root, message, duration=1400):
        message_label = ctk.CTkLabel(root, text=message, fg_color=("white", "gray38"))
        message_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        message_label.after(duration, message_label.destroy)

    def delete_password(service, master_password):
        passwords = load_passwords(master_password)
        if service in passwords:
            del passwords[service]
            save_passwords(passwords, master_password)
            return True
        return False

    def delete_password_action(service, master_password, scrollable_frame, root):
        # Create and display the input dialog
        dialog = ctk.CTkInputDialog(title="Confirm Deletion", text=f"To delete the password for '{service}', please type the service name and press OK.")

        svc = dialog.get_input()

        # Check the user's input
        if svc == service:  # Confirm the user has typed the exact service name
            if delete_password(service, master_password):
                show_temporary_message(root, f"Password for {service} deleted successfully!")
                refresh_list(scrollable_frame, master_password, root)
            else:
                show_temporary_message(root, "Error deleting password.")
        else:
            show_temporary_message(root, "Deletion cancelled. Incorrect service name.")
    
except Exception as e:
    print(f"An error occurred: {e}")
    messagebox.showerror("Error", "An error occurred. Please try again.")