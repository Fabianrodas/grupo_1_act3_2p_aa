import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from src.view.perfil import abrirVentanaPerfil

def login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    if usuario in usuariosValidos and usuariosValidos[usuario]["contraseña"] == contraseña:
        ventana.withdraw()  # Oculta ventana login
        usuarioInfo = usuariosValidos[usuario].copy()
        usuarioInfo["usuario"] = usuario
        abrirVentanaPerfil(usuarioInfo, ventana)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    
# Lista de usuarios del Portal:
usuariosValidos = {
    "paula.benalcazar": {
        "contraseña": "paulabenalcazar",
        "nombre": "PAULA MYLENNE BENALCÁZAR TORRES",
        "carrera": "INGENIERÍA EN CIENCIAS DE LA COMPUTACIÓN",
        "matricula": "2023240010",
        "cedula": "0901234567",
        "gpa": 91
    },
    "fabian.rodas": {
        "contraseña": "fabianrodas",
        "nombre": "FABIÁN EMMANUEL RODAS HIDALGO",
        "carrera": "INGENIERÍA EN CIENCIAS DE LA COMPUTACIÓN",
        "matricula": "2023240011",
        "cedula": "0904568766",
        "gpa": 89
    },
    "dylan.drouet": {
        "contraseña": "dylandrouet",
        "nombre": "DYLAN GABRIEL DROUET URETA",
        "carrera": "INGENIERÍA EN CIENCIAS DE LA COMPUTACIÓN",
        "matricula": "2023240012",
        "cedula": "0908765432",
        "gpa": 88
    },
    "luis.goncalves": {
        "contraseña": "luisgoncalves",
        "nombre": "LUIS FERNANDO GONCALVES LÓPEZ",
        "carrera": "INGENIERÍA EN CIENCIAS DE LA COMPUTACIÓN",
        "matricula": "2023240013",
        "cedula": "0902345678",
        "gpa": 90
    }
}

ventana = tk.Tk()
ventana.title("Portal de Servicios UEES")
ventana.geometry("750x550")  # Para cambiar el tamaño de la ventana
ventana.resizable(False, False) 
ventana.configure(bg="#7b002c")

# Frame izquierdo
frame_izquierdo = tk.Frame(ventana, width=500, bg="#7b002c") # Por si necesito cambiar el tamaño del lado izquierdo, modificar width
frame_izquierdo.pack(side="left", fill="both")


logo_path = "images/ueesLOGOBlanco.png"  
logo_img = Image.open(logo_path)
logo_img = logo_img.resize((190, 140))  # Con esto le cambio el tamaño al logo
logo = ImageTk.PhotoImage(logo_img)
tk.Label(frame_izquierdo, image=logo, bg="#7b002c").pack(pady=(20, 10))


tk.Label(frame_izquierdo, text="PORTAL DE SERVICIOS", font=("Helvetica", 12), fg="white", bg="#7b002c").pack(pady=20)

# Estas líneas son para simular un placeholder
def on_entry_click(event):
    if entry_usuario.get() == 'Usuario':
        entry_usuario.delete(0, "end")
        entry_usuario.config(fg='black')

def on_focusout(event):
    if entry_usuario.get() == '':
        entry_usuario.insert(0, 'Usuario')
        entry_usuario.config(fg='gray')

entry_usuario = tk.Entry(frame_izquierdo, font=("Helvetica", 12), fg='gray')
entry_usuario.insert(0, 'Usuario')
entry_usuario.bind('<FocusIn>', on_entry_click)
entry_usuario.bind('<FocusOut>', on_focusout)
entry_usuario.pack(pady=10, padx=20)

# Lo mismo pero para la contraseña
def on_pass_click(event):
    if entry_contraseña.get() == 'Contraseña':
        entry_contraseña.delete(0, "end")
        entry_contraseña.config(fg='black', show='*')

def on_pass_focusout(event):
    if entry_contraseña.get() == '':
        entry_contraseña.insert(0, 'Contraseña')
        entry_contraseña.config(fg='gray', show='')

entry_contraseña = tk.Entry(frame_izquierdo, font=("Helvetica", 12), fg='gray')
entry_contraseña.insert(0, 'Contraseña')
entry_contraseña.bind('<FocusIn>', on_pass_click)
entry_contraseña.bind('<FocusOut>', on_pass_focusout)
entry_contraseña.pack(pady=10, padx=20)

tk.Button(frame_izquierdo, text="INGRESAR", font=("Helvetica", 12, "bold"),
          command=login, bg="white", fg="#7b002c").pack(pady=20)

# Frame derecho
frame_derecho = tk.Frame(ventana, bg="lightgray")
frame_derecho.pack(side="right", fill="both", expand=True)

# Esto es el carrusel de la derecha
ruta_imagenes = [
    "images/ueesSlideOne.png",
    "images/ueesSlideTwo.png",
    "images/ueesSlideThree.png"
]

index_actual = 0
imagenes_originales = [Image.open(img) for img in ruta_imagenes]
imagenes_redimensionadas = [] 

def redimensionar_imagenes(ancho, alto):
    global imagenes_redimensionadas
    imagenes_redimensionadas = [
        ImageTk.PhotoImage(imagen.resize((ancho, alto)))
        for imagen in imagenes_originales
    ]


label_imagen = tk.Label(frame_derecho)
label_imagen.pack(fill="both", expand=True)

def iniciar_carrusel():
    ancho = frame_derecho.winfo_width()
    alto = frame_derecho.winfo_height()
    redimensionar_imagenes(ancho, alto)
    cambiar_imagen()
ventana.after(100, iniciar_carrusel)

def cambiar_imagen():
    global index_actual
    label_imagen.config(image=imagenes_redimensionadas[index_actual])
    index_actual = (index_actual + 1) % len(imagenes_redimensionadas)
    ventana.after(3000, cambiar_imagen)

ventana.mainloop()