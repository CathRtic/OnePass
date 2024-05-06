import customtkinter as ctk
import pyperclip
from tkinter import *
from password_generator import generate_password
from crypto import *


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
        show_temporary_message(root, "Password added successfully!")

def password_action(service):
    passwords = load_passwords(master_password)
    password = passwords.get(service)
    if password:
        pyperclip.copy(password)
        show_temporary_message(root, f"Password for {service} copied to clipboard!")

def generate_and_display_password():
    length = int(ctk.CTkInputDialog(title="Password Generator", text="Enter Password Length:").get_input())
    password = generate_password(length)
    password_entry.delete(0, END)  # Clear the entry widget first
    password_entry.insert(0, password)  # Insert the generated password

def show_temporary_message(root, message, duration=1400):
    message_label = ctk.CTkLabel(root, text=message, fg_color=("white", "gray38"))
    message_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
    message_label.after(duration, message_label.destroy)

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

#
# UI
#
initial_color_mode, initial_theme_mode = load_config()
ctk.set_appearance_mode(initial_color_mode)
ctk.set_default_color_theme(initial_theme_mode)

root = ctk.CTk() 
root.resizable(width=False, height=False)
root.title("OnePass")

settings = ctk.CTkFrame(master=root)
main = ctk.CTkFrame(master=root)

main.grid(row=0, column=0, sticky="nsew")
settings.grid(row=0, column=0, sticky="nsew")

dialog = ctk.CTkInputDialog(title="Password Manager", text="Enter your master password:")
master_password = dialog.get_input()  # This will wait for the user to input and press OK or Cancel

# Main Page
scrollable_frame = ctk.CTkScrollableFrame(main)
scrollable_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=20)

service_entry = ctk.CTkEntry(main, placeholder_text="Service Name")
service_entry.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

password_entry = ctk.CTkEntry(main, placeholder_text="Password")
password_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

add_button = ctk.CTkButton(main, text="Add Password", command=add_password)
add_button.grid(row=4, column=1, padx=20, pady=7)

generate_pass_button = ctk.CTkButton(main, text="Generate password", command=generate_and_display_password)
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

refresh_list()

root.mainloop()
