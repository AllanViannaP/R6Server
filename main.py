import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Pillow library for image handling

# Function to get the image path depending on whether it's a frozen executable or script
def get_image_path(image_name):
    if getattr(sys, 'frozen', False):
        # If running as a frozen executable, use the temp directory
        return os.path.join(sys._MEIPASS, image_name)
    else:
        # If running as a script, use the current directory
        return os.path.join(os.getcwd(), image_name)

# Function to automatically locate the GameSettings.ini file
def localizar_arquivo_automaticamente():
    try:
        base_path = fr"C:\Users\{os.getlogin()}\Documents\My Games\Rainbow Six - Siege"
        if not os.path.exists(base_path):
            raise FileNotFoundError("Base game folder not found.")
        
        subdirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        if len(subdirs) != 1:
            raise FileNotFoundError("Could not uniquely identify the subfolder.")
        
        # Access the only subfolder
        unique_folder = os.path.join(base_path, subdirs[0])
        file_path = os.path.join(unique_folder, "GameSettings.ini")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError("GameSettings.ini file not found.")
        
        entry_arquivo.delete(0, tk.END)
        entry_arquivo.insert(0, file_path)
        btn_salvar.config(state=tk.NORMAL)  # Enable the save button after file is found
    except Exception as e:
        messagebox.showerror(messages["error"], str(e))


# Function to alter the DataCenterHint value in the GameSettings.ini file
def alterar_datacenterhint():
    file_path = entry_arquivo.get()
    novo_valor = combobox_valores.get()
    
    if not os.path.exists(file_path):
        messagebox.showerror(messages["error"], messages["file_not_found_message"])
        return
    
    if not novo_valor.strip():
        messagebox.showerror(messages["error"], messages["choose_server_message"])
        return
    
    # Read the content of the file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find and modify the line with DataCenterHint
    for i, line in enumerate(lines):
        if line.startswith("DataCenterHint="):
            lines[i] = f"DataCenterHint={novo_valor}\n"
            break
    else:
        messagebox.showerror(messages["error"], messages["datacenterhint_not_found"])
        return
    
    # Write the changes back to the file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    messagebox.showinfo(messages["success"], f"Value changed to '{novo_valor}' successfully!")


# Function to change the language based on the selected language
def change_language(language):
    global messages
    
    if language == "English":
        messages = {
            "success": "Success",
            "error": "Error",
            "file_not_found": "GameSettings.ini file not found",
            "choose_server_message": "Please choose the server",
            "file_not_found_message": "File not found.",
            "datacenterhint_not_found": "DataCenterHint not found in the file.",
            "update_button": "Update",
            "locate_button": "Locate File",
            "file_insert_message": "Insert the server file"
        }
    elif language == "Portuguese":
        messages = {
            "success": "Sucesso",
            "error": "Erro",
            "file_not_found": "Arquivo GameSettings.ini não encontrado",
            "choose_server_message": "Por favor, escolha o servidor",
            "file_not_found_message": "Arquivo não encontrado.",
            "datacenterhint_not_found": "DataCenterHint não encontrado no arquivo.",
            "update_button": "Atualizar",
            "locate_button": "Localizar Arquivo",
            "file_insert_message": "Insira o arquivo do servidor"
        }
    elif language == "Spanish":
        messages = {
            "success": "Éxito",
            "error": "Error",
            "file_not_found": "Archivo GameSettings.ini no encontrado",
            "choose_server_message": "Por favor, elija el servidor",
            "file_not_found_message": "Archivo no encontrado.",
            "datacenterhint_not_found": "DataCenterHint no encontrado en el archivo.",
            "update_button": "Actualizar",
            "locate_button": "Localizar Archivo",
            "file_insert_message": "Inserte el archivo del servidor"
        }
    elif language == "Japanese":
        messages = {
            "success": "成功",
            "error": "エラー",
            "file_not_found": "GameSettings.ini ファイルが見つかりません",
            "choose_server_message": "サーバーを選んでください",
            "file_not_found_message": "ファイルが見つかりません",
            "datacenterhint_not_found": "GameSettings.ini に DataCenterHint が見つかりません",
            "update_button": "更新",
            "locate_button": "ファイルを探す",
            "file_insert_message": "サーバーファイルを挿入してください"
        }
    
    update_interface_text()


# Function to update all text in the interface based on the selected language
def update_interface_text():
    label_arquivo.config(text=messages["file_insert_message"])
    label_select_value.config(text=messages["choose_server_message"])
    btn_localizar.config(text=messages["locate_button"])
    btn_salvar.config(text=messages["update_button"])


# List of possible DataCenterHint values
valores_datacenter = [
    "default (ping based)",
    "playfab/australiaeast",
    "playfab/brazilsouth",
    "playfab/centralus",
    "playfab/eastasia",
    "playfab/eastus",
    "playfab/japaneast",
    "playfab/northeurope",
    "playfab/southafricanorth",
    "playfab/southcentralus",
    "playfab/southeastasia",
    "playfab/uaenorth",
    "playfab/westeurope",
    "playfab/westus",
]

# Initialize language to English
messages = {
    "success": "Success",
    "error": "Error",
    "file_not_found": "GameSettings.ini file not found",
    "choose_server_message": "Please choose the server",
    "file_not_found_message": "File not found.",
    "datacenterhint_not_found": "DataCenterHint not found in the file.",
    "update_button": "Update",
    "locate_button": "Locate File",
    "file_insert_message": "Insert the server file"
}

# Create the main application window
root = tk.Tk()
root.title("R6Server")  # Title change for the executable

# Set window size to a smaller width but keep the height as before (500x400)
root.geometry("540x500")  # Adjusted window size (narrower)
root.config(bg="#f4f4f4")

# Set the window icon
root.iconbitmap(get_image_path("r6_icon.ico"))

# Load flag images using Pillow
img_en = Image.open(get_image_path("us_flag.png")).resize((40, 30))
img_pt = Image.open(get_image_path("br_flag.png")).resize((40, 30))
img_es = Image.open(get_image_path("es_flag.png")).resize((40, 30))
img_jp = Image.open(get_image_path("jp_flag.png")).resize((40, 30))

# Convert images to Tkinter-compatible format
photo_en = ImageTk.PhotoImage(img_en)
photo_pt = ImageTk.PhotoImage(img_pt)
photo_es = ImageTk.PhotoImage(img_es)
photo_jp = ImageTk.PhotoImage(img_jp)

# Layout frame
frame = tk.Frame(root, padx=20, pady=20, bg="#f4f4f4")
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Language selection (flags at the top)
language_frame = tk.Frame(root, bg="#f4f4f4")
language_frame.pack(pady=(10, 0))

# Adding flag images as buttons at the top of the window
flag_en_button = tk.Button(language_frame, image=photo_en, command=lambda: change_language("English"), relief="flat", bg="#f4f4f4")
flag_en_button.grid(row=0, column=0, padx=10, pady=10)

flag_pt_button = tk.Button(language_frame, image=photo_pt, command=lambda: change_language("Portuguese"), relief="flat", bg="#f4f4f4")
flag_pt_button.grid(row=0, column=1, padx=10, pady=10)

flag_es_button = tk.Button(language_frame, image=photo_es, command=lambda: change_language("Spanish"), relief="flat", bg="#f4f4f4")
flag_es_button.grid(row=0, column=2, padx=10, pady=10)

flag_jp_button = tk.Button(language_frame, image=photo_jp, command=lambda: change_language("Japanese"), relief="flat", bg="#f4f4f4")
flag_jp_button.grid(row=0, column=3, padx=10, pady=10)

# Add the rest of the UI elements (labels, buttons, etc.)
label_arquivo = tk.Label(frame, text=messages["file_insert_message"], font=("Arial", 12), bg="#f4f4f4")
label_arquivo.grid(row=0, column=0, sticky="w", pady=10)

entry_arquivo = tk.Entry(frame, width=50, font=("Arial", 12), relief="solid", bd=2)
entry_arquivo.grid(row=1, column=0, pady=10)

btn_localizar = tk.Button(frame, text=messages["locate_button"], command=localizar_arquivo_automaticamente, font=("Arial", 12, "bold"), bg="#0275d8", fg="white", relief="flat", width=20)
btn_localizar.grid(row=2, column=0, columnspan=2, pady=20)

# Server selection
label_select_value = tk.Label(frame, text=messages["choose_server_message"], font=("Arial", 12, "bold"), bg="#f4f4f4", anchor="w")
label_select_value.grid(row=3, column=0, sticky="w", pady=10)

combobox_valores = ttk.Combobox(frame, values=valores_datacenter, font=("Arial", 12), width=40)
combobox_valores.grid(row=4, column=0, columnspan=2, pady=10)

# Button to save changes
btn_salvar = tk.Button(frame, text=messages["update_button"], command=alterar_datacenterhint, font=("Arial", 12, "bold"), bg="#0275d8", fg="white", relief="flat", width=20)
btn_salvar.grid(row=5, column=0, columnspan=2, pady=20)

# Start the application
root.mainloop()
