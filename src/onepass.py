import customtkinter as ctk
from tkinter import END
import pyperclip
from password_generator import generate_password
from crypto import *
import customtkinter as ctk
import tkinter.messagebox as messagebox
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['OnePass']
collection = db['passwords']

try:
    def load_passwords(master_password):
        passwords = {}
        for doc in collection.find():
            service = doc['service']
            encrypted_password = doc['password']
            password = decrypt_data(encrypted_password, master_password)
            if password:
                passwords[service] = password
        return passwords


    def save_passwords(data, master_password):
        for service, password in data.items():
            encrypted_password = encrypt_data(password, master_password)
            collection.update_one(
                {'service': service},
                {'$set': {'password': encrypted_password}},
                upsert=True
            )

    def refresh_list(scrollable_frame, master_password, root):
        passwords = load_passwords(master_password)
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        for service in passwords:
            row_frame = ctk.CTkFrame(scrollable_frame)
            row_frame.pack(pady=2, padx=10, fill=ctk.X)

            service_button = ctk.CTkButton(row_frame, text=service,
                                        command=lambda svc=service: password_action(svc, master_password, root))
            service_button.pack(side='left', expand=True, fill=ctk.X, padx=5)

            delete_button = ctk.CTkButton(row_frame, text='X', width=5, fg_color='#bd1919',
                                        command=lambda svc=service: delete_password_action(svc, master_password, scrollable_frame, root))
            delete_button.pack(side='right')

    def add_password(service_entry, password_entry, master_password, scrollable_frame, root):
        service = service_entry.get().strip()
        password = password_entry.get().strip()
        if service and password:
            data = load_passwords(master_password)
            data[service] = password
            save_passwords(data, master_password)
            refresh_list(scrollable_frame, master_password, root)
            service_entry.delete(0, END)
            password_entry.delete(0, END)
        else:
            messagebox.showerror("Error", "Service and Password cannot be empty")



    def password_action(service, master_password, root):
        passwords = load_passwords(master_password)
        if service in passwords:
            pyperclip.copy(passwords[service])
            messagebox.showinfo("Password copied", f"Password for {service} has been copied to clipboard")

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

    def delete_password_action(service, master_password, scrollable_frame, root):
        collection.delete_one({'service': service})
        refresh_list(scrollable_frame, master_password, root)

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


    def switch_appearance_mode():
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Light":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    # Function to save the chosen color mode and theme to a configuration file
    def save_config(color_mode, theme_mode):
        with open('config.txt', 'w') as f:
            f.write(f"{color_mode},{theme_mode}")

    # Function to load the saved color mode and theme from the configuration file
    def load_config():
        try:
            with open('config.txt', 'r') as f:
                return f.read().split(',')
        except FileNotFoundError:
            return "System", "blue"  # Default mode and theme if the configuration file doesn't exist

    # Function to set the appearance mode and save the selected mode
    def color_button_callback(value):
        ctk.set_appearance_mode(value)
        save_config(value, theme_button_var.get())

    # Function to set the theme mode and save the selected theme
    def theme_button_callback(value, duration = 2200):
        ctk.set_default_color_theme(value)
        save_config(color_button_var.get(), value)
        message_label = ctk.CTkLabel(root, text="Change will take effect on app restart", fg_color=("white", "gray38"))
        message_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        message_label.after(duration, message_label.destroy)

except Exception as e:
    print(f"An error occurred: {e}")
    messagebox.showerror("Error", "An error occurred. Please try again.")


root = ctk.CTk()
root.resizable(width=False, height=False)
root.title("OnePass")

initial_color_mode, initial_theme_mode = load_config()
ctk.set_appearance_mode(initial_color_mode)
ctk.set_default_color_theme(initial_theme_mode)

# Main and settings frame
settings = ctk.CTkFrame(master=root)
main = ctk.CTkFrame(master=root)
main.grid(row=0, column=0, sticky="nsew")
settings.grid(row=0, column=0, sticky="nsew")

# Dialog for master password
dialog = ctk.CTkInputDialog(title="OnePass", text="Enter your master password:")
master_password = dialog.get_input()  # This will wait for the user to input and press OK or Cancel

# Main Page
scrollable_frame = ctk.CTkScrollableFrame(main)
scrollable_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=20)

service_entry = ctk.CTkEntry(main, placeholder_text="Service Name")
service_entry.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

password_entry = ctk.CTkEntry(main, placeholder_text="Password", show='*')
password_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

add_button = ctk.CTkButton(main, text="Add Password", command=lambda: add_password(service_entry, password_entry, master_password, scrollable_frame, root))

add_button.grid(row=4, column=1, padx=20, pady=7)

generate_pass_button = ctk.CTkButton(main, text="Generate Password", command=lambda: generate_and_display_password(password_entry, root))
generate_pass_button.grid(row=4, column=0, padx=20, pady=7)

settings_button = ctk.CTkButton(main, text="Settings", command=lambda: settings.tkraise())
settings_button.grid(row=5, column=0, columnspan=2, padx=20, pady=5)



# Settings Page
label = ctk.CTkLabel(settings, text="Color Mode", fg_color="transparent")
label.pack(fill = ctk.X, padx=20, pady=5)

color_button_var = ctk.StringVar(value=initial_color_mode)
color_button = ctk.CTkSegmentedButton(settings, values=["System", "Dark", "Light"], variable=color_button_var, command=color_button_callback)
color_button.pack(fill = ctk.X, padx=20, pady=5)

label = ctk.CTkLabel(settings, text="Theme", fg_color="transparent")
label.pack(fill = ctk.X, padx=20, pady=5)

theme_button_var = ctk.StringVar(value=initial_theme_mode)
theme_button = ctk.CTkSegmentedButton(settings, values=["blue", "green"], variable=theme_button_var, command=theme_button_callback)
theme_button.pack(fill = ctk.X, padx=20, pady=5)

main_button = ctk.CTkButton(settings, text="Back to Main", command=lambda: main.tkraise())
main_button.pack(fill = ctk.X, padx=20, pady=20)

refresh_list(scrollable_frame, master_password, root)
root.mainloop()