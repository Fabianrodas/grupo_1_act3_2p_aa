import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def abrirVentanaPerfil(usuarioInfo, ventana_login):
    perfil_ventana = tk.Toplevel()
    perfil_ventana.title("Perfil del Estudiante")
    perfil_ventana.geometry("1000x850")
    perfil_ventana.configure(bg="white")

    # Barra superior 
    barra_superior = tk.Frame(perfil_ventana, bg="#7b002c", height=80)
    barra_superior.pack(fill="x", side="top")

    logo_path = Path(__file__).resolve().parents[2] / "images" / "ueesLOGOBlanco.png"
    try:
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((160, 50), Image.LANCZOS)
        logo_tk = ImageTk.PhotoImage(logo_img)
        tk.Label(barra_superior, image=logo_tk, bg="#7b002c").pack(side="left", padx=10, pady=5)
    except Exception as e:
        print(f"Error cargando logo: {e}")
        tk.Label(barra_superior, text="UEES", font=("Helvetica", 12, "bold"),
                 bg="#7b002c", fg="white").pack(side="left", padx=10)

    opciones_usuario = tk.Menu(perfil_ventana, tearoff=0)
    opciones_usuario.add_command(label="Cerrar Sesión", command=lambda: cerrar_ventana(perfil_ventana, ventana_login))

    def mostrar_menu(event):
        opciones_usuario.tk_popup(event.x_root, event.y_root)

    usuario_texto = f"{usuarioInfo['usuario']}  ▼"
    usuario_btn = tk.Label(barra_superior, text=usuario_texto, font=("Helvetica", 10),
                        fg="white", bg="#7b002c", cursor="hand2", padx=10, pady=5)
    usuario_btn.pack(side="right", padx=20)
    usuario_btn.bind("<Button-1>", mostrar_menu)

    def on_hover(event):
        usuario_btn.config(bg="#5a001f")

    def on_leave(event):
        usuario_btn.config(bg="#7b002c")

    usuario_btn.bind("<Enter>", on_hover)
    usuario_btn.bind("<Leave>", on_leave)

    frame = tk.Frame(perfil_ventana, bg="white")
    frame.pack(fill="both", expand=True)

    # Foto del estudiante IMPORTANTE!!! = (ESTA PARTE HAY QUE MODIFIFCAR PARA QUE YA APAREZCAN DE UNA LAS FOTOS DE CADA UNO)
    canvas = tk.Canvas(frame, width=120, height=120, bg="white", highlightthickness=1, highlightbackground="black")
    canvas.place(x=50, y=40)

    def insertar_imagen():
        file_path = filedialog.askopenfilename()
        if file_path:
            img = Image.open(file_path)
            img = img.resize((120, 120))
            img = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, anchor="nw", image=img)
            canvas.image = img  

    insertar_btn = tk.Button(frame, text="Insertar imagen\no imagen default", command=insertar_imagen)
    insertar_btn.place(x=60, y=80)

    # Info del estudiante
    tk.Label(frame, text=usuarioInfo["nombre"], font=("Helvetica", 12, "bold"), bg="white").place(x=200, y=40)
    tk.Label(frame, text="CARRERA:", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=200, y=80)
    tk.Label(frame, text=usuarioInfo['carrera'], font=("Helvetica", 10), bg="white").place(x=280, y=80)
    tk.Label(frame, text="MATRÍCULA:", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=200, y=105)
    tk.Label(frame, text=usuarioInfo['matricula'], font=("Helvetica", 10), bg="white").place(x=285, y=105)
    tk.Label(frame, text="CÉDULA:", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=200, y=130)
    tk.Label(frame, text=usuarioInfo['cedula'], font=("Helvetica", 10), bg="white").place(x=260, y=130)
    tk.Label(frame, text="GPA:", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=200, y=155)
    tk.Label(frame, text=usuarioInfo['gpa'], font=("Helvetica", 10), bg="white").place(x=235, y=155)

    # Contenido para la malla curricular (bordes y la foto con fotos generadas de malla.py)
    tk.Label(frame, text="MALLA CURRICULAR", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=30, y=220)
    frame_malla = tk.Frame(frame, bg="white", bd=3, relief="solid", width=750, height=500)
    frame_malla.place(x=30, y=245)

    malla_path = Path(__file__).resolve().parents[2] / "malla.png"
    if malla_path.exists():
        try:
            img = Image.open(malla_path)
            img.thumbnail((900, 480))
            img_tk = ImageTk.PhotoImage(img)
            malla_label = tk.Label(frame_malla, image=img_tk, bg="white")
            malla_label.image = img_tk  
            malla_label.place(x=10, y=10)
        except Exception as e:
            print("Error cargando la imagen de malla:", e)

    perfil_ventana.logo = logo_tk if 'logo_tk' in locals() else None

def cerrar_ventana(ventana, ventana_login):
    ventana.destroy()
    ventana_login.deiconify()
