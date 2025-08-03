import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from src.utils.consts import *
from src.utils.malla import getMalla, dibujarMalla, dibujarPrerequisitos
from src.logic.dfs import DFS_prerequisitos
from src.logic.bfs import BFS_prerequisitos

def normaliza_nombre(nombre):
    t = str.maketrans("áéíóúñÁÉÍÓÚ", "aeiounAEIOU")
    return nombre.translate(t).replace(" ", "_")

def obtener_imagen_prerequisitos(materia):
    nombre_img = normaliza_nombre(materia)
    return Path(f"prerequisitos_{nombre_img}.png")

def abrirVentanaPerfil(usuarioInfo, ventana_login):
    perfil_ventana = tk.Toplevel()
    perfil_ventana.title("Perfil del Estudiante")
    perfil_ventana.state('zoomed')
    perfil_ventana.resizable(False, False)
    perfil_ventana.configure(bg="white")
    
    def cerrar_todo():
        perfil_ventana.destroy()
        ventana_login.destroy()  # Esto cierra todo el programa

    # Captura la X de la ventana
    perfil_ventana.protocol("WM_DELETE_WINDOW", cerrar_todo)

    # Barra superior
    barra_superior = tk.Frame(perfil_ventana, bg="#7b002c", height=80)
    barra_superior.pack(fill="x", side="top")

    logo_path = Path(__file__).resolve().parents[2] / "images" / "ueesLOGOBlanco.png"
    try:
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((160, 50), Image.LANCZOS)
        logo_tk = ImageTk.PhotoImage(logo_img)
        tk.Label(barra_superior, image=logo_tk, bg="#7b002c").pack(side="left", padx=10, pady=5)
    except:
        tk.Label(barra_superior, text="UEES", font=("Helvetica", 12, "bold"),
                 bg="#7b002c", fg="white").pack(side="left", padx=10)

    # Menú usuario
    opciones_usuario = tk.Menu(perfil_ventana, tearoff=0)
    opciones_usuario.add_command(label="Cerrar Sesión", command=lambda: cerrar_ventana(perfil_ventana, ventana_login))

    def mostrar_menu(event):
        opciones_usuario.tk_popup(event.x_root, event.y_root)

    usuario_texto = f"{usuarioInfo['usuario']}  ▼"
    usuario_btn = tk.Label(barra_superior, text=usuario_texto, font=("Helvetica", 10),
                           fg="white", bg="#7b002c", cursor="hand2", padx=10, pady=5)
    usuario_btn.pack(side="right", padx=20)
    usuario_btn.bind("<Button-1>", mostrar_menu)

    # Hover
    usuario_btn.bind("<Enter>", lambda e: usuario_btn.config(bg="#5a001f"))
    usuario_btn.bind("<Leave>", lambda e: usuario_btn.config(bg="#7b002c"))

    # Frame general
    frame = tk.Frame(perfil_ventana, bg="white")
    frame.pack(fill="both", expand=True)

    # Foto estudiante
    canvas = tk.Canvas(frame, width=140, height=140, bg="white", highlightthickness=1, highlightbackground="black")
    canvas.place(x=50, y=40)

    user_photo_path = Path(__file__).resolve().parents[2] / "images" / f"{usuarioInfo['usuario']}.jpg"
    try:
        img = Image.open(user_photo_path)
    except FileNotFoundError:
        img = Image.open(Path(__file__).resolve().parents[2] / "images" / "default.jpg")

    img = img.resize((140, 140))
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk  

    # Info estudiante
    tk.Label(frame, text=usuarioInfo["nombre"], font=("Helvetica", 12, "bold"), bg="white").place(x=200, y=40)
    tk.Label(frame, text="CARRERA:", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=200, y=80)
    tk.Label(frame, text=usuarioInfo['carrera'], font=("Helvetica", 10), bg="white").place(x=270, y=80)
    tk.Label(frame, text="MATRÍCULA:", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=200, y=105)
    tk.Label(frame, text=usuarioInfo['matricula'], font=("Helvetica", 10), bg="white").place(x=285, y=105)
    tk.Label(frame, text="CÉDULA:", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=200, y=130)
    tk.Label(frame, text=usuarioInfo['cedula'], font=("Helvetica", 10), bg="white").place(x=260, y=130)
    tk.Label(frame, text="GPA:", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=200, y=155)
    tk.Label(frame, text=usuarioInfo['gpa'], font=("Helvetica", 10), bg="white").place(x=235, y=155)

    # Lista de materias
    materias_lista = []
    for materias in SEMESTRES.values():
        materias_lista.extend(materias)
    materias_lista.sort()

    # Panel malla
    tk.Label(frame, text="MALLA CURRICULAR", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=30, y=220)
    frame_malla = tk.Frame(frame, bg="white", bd=3, relief="solid")
    frame_malla.place(relx=0.03, rely=0.33, relwidth=0.52, relheight=0.62)
    frame_malla.pack_propagate(False)

    malla_canvas = tk.Canvas(frame_malla, width=1045, height=700, bg="white", highlightthickness=0)
    malla_canvas.pack(fill="both", expand=True)

    h_scroll = tk.Scrollbar(frame_malla, orient="horizontal", command=malla_canvas.xview)
    v_scroll = tk.Scrollbar(frame_malla, orient="vertical", command=malla_canvas.yview)
    malla_canvas.config(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
    h_scroll.pack(side="bottom", fill="x")
    v_scroll.pack(side="right", fill="y")

    right_panel = tk.Frame(frame, bg="white", width=350, height=500)
    right_panel.pack(side="right", padx=250, pady=(0,220)) 
    right_panel.pack_propagate(False)

    # Tipo de algoritmo
    tk.Label(right_panel, text="TIPO DE ALGORITMO:", font=("Helvetica", 14, "bold"),
             bg="#7b002c", fg="white", width=30).pack(pady=15)
    algoritmo_var = tk.StringVar(value="DFS")
    tk.Radiobutton(right_panel, text="BFS", variable=algoritmo_var, value="BFS", bg="white", font=("Helvetica", 12)).pack(anchor="w", padx=40)
    tk.Radiobutton(right_panel, text="DFS", variable=algoritmo_var, value="DFS", bg="white", font=("Helvetica", 12)).pack(anchor="w", padx=40)

    # Recorrer por
    tk.Label(right_panel, text="RECORRER POR:", font=("Helvetica", 14, "bold"),
             bg="#7b002c", fg="white", width=30).pack(pady=15)
    recorrido_var = tk.StringVar(value="Pre-requisitos")
    tk.Radiobutton(right_panel, text="Pre-requisitos", variable=recorrido_var, value="Pre-requisitos", bg="white", font=("Helvetica", 12)).pack(anchor="w", padx=40)
    tk.Radiobutton(right_panel, text="Post-requisitos", variable=recorrido_var, value="Post-requisitos", bg="white", font=("Helvetica", 12)).pack(anchor="w", padx=40)

    # Seleccionar materia
    tk.Label(right_panel, text="SELECCIONAR MATERIA:", font=("Helvetica", 14, "bold"),
             bg="#7b002c", fg="white", width=30).pack(pady=15)
    combo_materias = ttk.Combobox(right_panel, values=["Selecciona una materia"] + materias_lista, state="readonly", font=("Helvetica", 13), width=28)
    combo_materias.set("Selecciona una materia")
    combo_materias.pack(pady=10)

    def enviar_accion():
        materia = combo_materias.get()
        if materia == "Selecciona una materia":
            mostrar_malla_general()
            return

        algoritmo = algoritmo_var.get()
        recorrido = recorrido_var.get()

        if recorrido == "Post-requisitos":
            malla_canvas.delete("all")
            malla_canvas.create_text(20, 20, anchor="nw", text="Aún no está implementada.", fill="black")
            return

        G = getMalla()
        prereqs = BFS_prerequisitos(G, materia) if algoritmo == "BFS" else DFS_prerequisitos(G, materia)
        prereqs = list(prereqs)

        ruta_img = obtener_imagen_prerequisitos(materia)
        ok = dibujarPrerequisitos(G, materia, prereqs)
        if ok and ruta_img.exists():
            cargar_y_mostrar_imagen(str(ruta_img))
        else:
            malla_canvas.delete("all")
            malla_canvas.create_text(20, 20, anchor="nw", text=f"No se pudo generar imagen para:\n{materia}", fill="black")

    enviar_btn = tk.Button(right_panel, text="Enviar", font=("Helvetica", 13, "bold"),
                           bg="#7b002c", fg="white", width=18, height=2, command=enviar_accion)
    enviar_btn.pack(pady=10)

    descargar_btn = tk.Button(right_panel, text="Descargar Benchmark", font=("Helvetica", 13, "bold"),
                              bg="#7b002c", fg="white", width=18, height=2) 
    descargar_btn.pack(pady=10)

    # Funciones de la malla
    G = getMalla()
    malla_path = Path("malla.png")
    if not malla_path.exists():
        dibujarMalla(G)

    malla_img = None
    scale_factor = 0.6

    def cargar_y_mostrar_imagen(path, reset_zoom=True):
        nonlocal malla_img, scale_factor
        try:
            img = Image.open(path)
            if reset_zoom:
                scale_factor = 0.6
            w, h = int(img.width * scale_factor), int(img.height * scale_factor)
            img = img.resize((w, h), Image.LANCZOS)
            
            malla_img = ImageTk.PhotoImage(img)
            malla_canvas.delete("all")
            malla_canvas.imgtk = malla_img  
            malla_canvas.create_image(0, 0, anchor="nw", image=malla_img)
            malla_canvas.config(scrollregion=malla_canvas.bbox("all"))
            malla_canvas.current_image_path = path
        except:
            malla_canvas.delete("all")
            malla_canvas.create_text(20, 20, anchor="nw", text=f"Error cargando imagen", fill="black")

    def mostrar_malla_general():
        cargar_y_mostrar_imagen(str(malla_path))

    mostrar_malla_general()

    def zoom(event):
        nonlocal scale_factor
        if malla_img is None:
            return
        if event.delta > 0 or event.num == 4:
            scale_factor *= 1.1
        elif event.delta < 0 or event.num == 5:
            scale_factor /= 1.1
        scale_factor = max(0.2, min(scale_factor, 3.0))
        cargar_y_mostrar_imagen(malla_canvas.current_image_path, reset_zoom=False)

    malla_canvas.bind("<MouseWheel>", zoom)
    malla_canvas.bind("<Button-4>", zoom)  
    malla_canvas.bind("<Button-5>", zoom)  

    perfil_ventana.logo = logo_tk if 'logo_tk' in locals() else None

def cerrar_ventana(ventana, ventana_login):
    ventana.destroy()
    ventana_login.deiconify()
