import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

# Estas líneas solo las puse para testeo, se cambiarán cuando se cree la otra ventana 
    # if usuario == "paula.benalcazar" and contraseña == "1234":
    #    messagebox.showinfo("Login Exitoso", f"Bienvenida, {usuario}")
    # else:
    #    messagebox.showerror("Error", "Usuario o contraseña incorrectos")


ventana = tk.Tk()
ventana.title("Portal de Servicios UEES")
ventana.geometry("1000x550")  # Para cambiar el tamaño de la ventana
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


label_imagen = tk.Label(frame_derecho, bg="lightgray")
label_imagen.pack(fill="both", expand=True)

def iniciar_carrusel(event=None):
    ancho = frame_derecho.winfo_width()
    alto = frame_derecho.winfo_height()
    redimensionar_imagenes(ancho, alto)
    cambiar_imagen()
frame_derecho.bind("<Configure>", iniciar_carrusel)

index_actual = 0

def cambiar_imagen():
    global index_actual
    label_imagen.config(image=imagenes_redimensionadas[index_actual])
    index_actual = (index_actual + 1) % len(imagenes_redimensionadas)
    ventana.after(3000, cambiar_imagen)

ventana.mainloop()