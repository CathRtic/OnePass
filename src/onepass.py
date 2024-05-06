import customtkinter as ctk
from tkinter import END
from password_manager import add_password, generate_and_display_password, refresh_list, show_temporary_message, password_action
import tkinter as tk


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

password_entry = ctk.CTkEntry(main, placeholder_text="Password")
password_entry.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

add_button = ctk.CTkButton(main, text="Add Password", command=lambda: add_password(service_entry, password_entry, master_password, scrollable_frame, root))

add_button.grid(row=4, column=1, padx=20, pady=7)

generate_pass_button = ctk.CTkButton(main, text="Generate Password", command=lambda: generate_and_display_password(password_entry))
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


