import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from src.utils.consts import SEMESTRES
from src.utils.malla import getMalla, dibujarMalla, dibujarPrerequisitos, obtener_info_materia
from src.logic.dfs import DFS_prerequisitos

def normaliza_nombre(nombre):
    t = str.maketrans("áéíóúñÁÉÍÓÚ", "aeiounAEIOU")
    return nombre.translate(t).replace(" ", "_")

def obtener_imagen_prerequisitos(materia):
    nombre_img = normaliza_nombre(materia)
    return Path(f"prerequsitos_{nombre_img}.png")

def abrirVentanaPerfil(usuarioInfo, ventana_login):
    perfil_ventana = tk.Toplevel()
    perfil_ventana.title("Perfil del Estudiante")
    perfil_ventana.state('zoomed')
    perfil_ventana.resizable(False, False)
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

    # Foto del estudiante
    canvas = tk.Canvas(frame, width=140, height=140, bg="white", highlightthickness=1, highlightbackground="black")
    canvas.place(x=50, y=40)

    # Ruta de imagen automática según el usuario
    user_photo_path = Path(__file__).resolve().parents[2] / "images" / f"{usuarioInfo['usuario']}.jpg"

    try:
        img = Image.open(user_photo_path)
    except FileNotFoundError:
        # Imagen default si no existe foto personalizada
        img = Image.open(Path(__file__).resolve().parents[2] / "images" / "default.jpg")

    img = img.resize((140, 140))
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk  

    # Info del estudiante
    tk.Label(frame, text=usuarioInfo["nombre"], font=("Helvetica", 12, "bold"), bg="white").place(x=200, y=40)
    tk.Label(frame, text="CARRERA:", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=200, y=80)
    tk.Label(frame, text=usuarioInfo['carrera'], font=("Helvetica", 10), bg="white").place(x=270, y=80)
    tk.Label(frame, text="MATRÍCULA:", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=200, y=105)
    tk.Label(frame, text=usuarioInfo['matricula'], font=("Helvetica", 10), bg="white").place(x=285, y=105)
    tk.Label(frame, text="CÉDULA:", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=200, y=130)
    tk.Label(frame, text=usuarioInfo['cedula'], font=("Helvetica", 10), bg="white").place(x=260, y=130)
    tk.Label(frame, text="GPA:", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=200, y=155)
    tk.Label(frame, text=usuarioInfo['gpa'], font=("Helvetica", 10), bg="white").place(x=235, y=155)

    materias_lista = []
    for materias in SEMESTRES.values():
        materias_lista.extend(materias)
    materias_lista.sort()

    # Panel de la malla a la izquierda
    tk.Label(frame, text="MALLA CURRICULAR", font=("Helvetica", 10, "bold"), fg="#801434", bg="white").place(x=30, y=220)
    frame_malla = tk.Frame(frame, bg="white", bd=3, relief="solid", width=1050, height=700)
    frame_malla.place(x=30, y=245)
    frame_malla.pack_propagate(False)

    malla_canvas = tk.Canvas(frame_malla, width=1045, height=695, bg="white", highlightthickness=0)
    malla_canvas.pack(fill="both", expand=True)

    # Scrollbars
    h_scroll = tk.Scrollbar(frame_malla, orient="horizontal", command=malla_canvas.xview)
    v_scroll = tk.Scrollbar(frame_malla, orient="vertical", command=malla_canvas.yview)
    malla_canvas.config(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
    h_scroll.pack(side="bottom", fill="x")
    v_scroll.pack(side="right", fill="y")

    # Panel derecho (combobox + info)
    right_panel = tk.Frame(frame, bg="white")
    right_panel.place(x=1150, y=245)

    combo_materias = ttk.Combobox(
        right_panel,
        values=["Selecciona una materia"] + materias_lista,
        state="readonly",
        font=("Helvetica", 13),
        width=28
    )
    combo_materias.set("Selecciona una materia")
    combo_materias.grid(row=0, column=0, padx=5, pady=10)

    info_label = tk.Label(
        right_panel,
        text="",
        font=("Helvetica", 13),
        bg="white",
        anchor="nw",
        justify="left",
        fg="#7b002c"
    )
    info_label.grid(row=1, column=0, sticky="nw")

    G = getMalla()

    malla_path = Path("malla.png")
    if not malla_path.exists():
        dibujarMalla(G)
    malla_img = None

    scale_factor = 1.0
    malla_canvas.imgtk = None
    
    def cargar_y_mostrar_imagen(path, reset_zoom=True):
        nonlocal malla_img, scale_factor
        try:
            img = Image.open(path)
            if reset_zoom:
                scale_factor = 0.3
            w, h = int(img.width * scale_factor), int(img.height * scale_factor)
            img = img.resize((w, h), Image.LANCZOS)
            
            malla_img = ImageTk.PhotoImage(img)
            malla_canvas.delete("all")
            malla_canvas.imgtk = malla_img  
            malla_canvas.create_image(0, 0, anchor="nw", image=malla_img)
            malla_canvas.config(scrollregion=malla_canvas.bbox("all"))
        except Exception as e:
            malla_canvas.delete("all")
            malla_canvas.create_text(20, 20, anchor="nw", text=f"Error cargando imagen", fill="black")

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

    def mostrar_malla_general():
        malla_canvas.current_image_path = str(malla_path)
        cargar_y_mostrar_imagen(malla_canvas.current_image_path)

    mostrar_malla_general()

    def mostrar_prerequisitos(event):
        materia = combo_materias.get()
        if materia == "Selecciona una materia":
            mostrar_malla_general()
            info_label.config(text="")
            return

        prereqs = DFS_prerequisitos(G, materia)
        prereqs = list(prereqs - {materia}) if materia in prereqs else list(prereqs)

        ruta_img = obtener_imagen_prerequisitos(materia)
        ok = dibujarPrerequisitos(G, materia, prereqs)
        if ok and ruta_img.exists():
            malla_canvas.current_image_path = str(ruta_img)
            cargar_y_mostrar_imagen(malla_canvas.current_image_path)
        else:
            malla_canvas.delete("all")
            malla_canvas.create_text(20, 20, anchor="nw",
                                    text=f"No se pudo generar imagen para:\n{materia}", fill="black")

        info = obtener_info_materia(G, materia)
        if isinstance(info, dict) and "Error" not in info:
            texto = (
                f"CÓDIGO: {info.get('Código','N/A')}\n"
                f"PROFESOR: {info.get('Profesor','No registrado')}\n"
                f"HORARIO: {info.get('Horario','No registrado')}"
            )
            info_label.config(text=texto)
        else:
            info_label.config(text="No hay información registrada para esta materia.")

    combo_materias.bind("<<ComboboxSelected>>", mostrar_prerequisitos)
    perfil_ventana.logo = logo_tk if 'logo_tk' in locals() else None

def cerrar_ventana(ventana, ventana_login):
    ventana.destroy()
    ventana_login.deiconify()
