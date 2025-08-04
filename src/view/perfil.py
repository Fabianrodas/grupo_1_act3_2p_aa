import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from src.utils.consts import *
from src.utils.malla import getMalla, dibujarMalla, dibujarPrerequisitos, obtener_info_materia
from src.logic.dfs import DFS_prerequisitos, DFS_postrequisitos
from src.logic.bfs import BFS_prerequisitos, BFS_postrequisitos
from src.view.planificador import abrir_ventana_planificador
from src.model.benchmark import sortResults
import timeit
import pandas as pd
import psutil
import winreg
import os
import platform

def normaliza_nombre(nombre):
    t = str.maketrans("áéíóúñÁÉÍÓÚ", "aeiounAEIOU")
    return nombre.translate(t).replace(" ", "_")

def obtener_imagen_prerequisitos(materia):
    nombre_img = normaliza_nombre(materia)
    return Path(f"prerequisitos_{nombre_img}.png")

def obtener_imagen_postrequisitos(materia):
    nombre_img = normaliza_nombre(materia)
    return Path(f"postrequisitos_{nombre_img}.png")

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

    # Inicalizar malla
    G = getMalla()
    malla_path = Path("malla.png")
    if not malla_path.exists():
        dibujarMalla(G)

    # Frame para el botón de reset zoom, colocado justo debajo del frame_malla
    frame_reset = tk.Frame(frame, bg="white")
    frame_reset.place(relx=0.03, rely=0.95)  # Ajusta 'rely' para que quede debajo de frame_malla

    # Botón para resetear el zoom de la imagen de la malla (última imagen mostrada)
    malla_path = Path("malla.png")
    ultima_ruta_img = [str(malla_path)] 

    reset_zoom_btn = tk.Button(
        frame_reset,
        text="Resetear Zoom",
        font=("Helvetica", 11, "bold"),
        bg="#801434",
        fg="white",
        command=lambda: cargar_y_mostrar_imagen(ultima_ruta_img[0], reset_zoom=True)
    )
    reset_zoom_btn.pack()

    # ============================
    # PANEL DERECHO ANCHO Y ESTÉTICO
    # ============================

    right_panel = tk.Frame(frame, bg="white", width=500, height=1000)  
    right_panel.pack(side="right", anchor="n", padx=50, pady=10)
    right_panel.pack_propagate(False)

    # ---------- SECCIÓN 1: Información extra ----------
    info_frame = tk.LabelFrame(
        right_panel,
        text="Información extra de la materia",
        bg="white",
        font=("Helvetica", 12, "bold"),
        padx=10, pady=5,
        width=380, height=150
    )
    info_frame.pack(fill="x", pady=15, padx=10)
    info_frame.pack_propagate(False) 

    campos = ["Materia", "Código", "Profesor", "Horario"]
    labels_info = {}

    for campo in campos:
        fila = tk.Frame(info_frame, bg="white")
        fila.pack(fill="x", pady=3)
        lbl_campo = tk.Label(fila, text=f"{campo}:", width=12, anchor="w", bg="white", font=("Helvetica", 10, "bold"))
        lbl_campo.pack(side="left")
        lbl_valor = tk.Label(fila, text="---", bg="white", anchor="w", font=("Helvetica", 10))
        lbl_valor.pack(side="left", fill="x", expand=True)
        labels_info[campo] = lbl_valor

    # ---------- SECCIÓN 2-3-4 + BOTONES ----------
    param_frame = tk.LabelFrame(
        right_panel,
        text="Parámetros de Búsqueda",
        bg="white",
        font=("Helvetica", 12, "bold"),
        padx=10, pady=10,
        width=380, height=300
    )
    param_frame.pack(fill="x", pady=15, padx=10)
    param_frame.pack_propagate(False)
    
    btn_frame = tk.Frame(right_panel, bg="white")
    btn_frame.pack(fill="x", pady=15, padx=10)

    btn_frame.config(height=1220)     
    btn_frame.pack_propagate(False)

    btn_style = {
        "font": ("Helvetica", 13, "bold"),
        "bg": "#7b002c",
        "fg": "white",
        "height": 2
    }

    # --- Tipo de Algoritmo ---
    tk.Label(param_frame, text="Tipo de Algoritmo", font=("Helvetica", 11, "bold"), bg="white").pack(anchor="w", pady=(0,5))
    algoritmo_var = tk.StringVar(value="DFS")
    tk.Radiobutton(param_frame, text="BFS", variable=algoritmo_var, value="BFS", bg="white", font=("Helvetica", 10)).pack(anchor="w", padx=20)
    tk.Radiobutton(param_frame, text="DFS", variable=algoritmo_var, value="DFS", bg="white", font=("Helvetica", 10)).pack(anchor="w", padx=20)

    # --- Recorrer por ---
    tk.Label(param_frame, text="Recorrer por", font=("Helvetica", 11, "bold"), bg="white").pack(anchor="w", pady=(10,5))
    recorrido_var = tk.StringVar(value="Pre-requisitos")
    tk.Radiobutton(param_frame, text="Pre-requisitos", variable=recorrido_var, value="Pre-requisitos", bg="white", font=("Helvetica", 10)).pack(anchor="w", padx=20)
    tk.Radiobutton(param_frame, text="Post-requisitos", variable=recorrido_var, value="Post-requisitos", bg="white", font=("Helvetica", 10)).pack(anchor="w", padx=20)

    # --- Selección de materia ---
    tk.Label(param_frame, text="Seleccionar Materia", font=("Helvetica", 11, "bold"), bg="white").pack(anchor="w", pady=(10,5))
    combo_materias = ttk.Combobox(
        param_frame,
        values=["Selecciona una materia"] + materias_lista,
        state="readonly",
        font=("Helvetica", 12),
        width=30  # Más ancho
    )
    combo_materias.set("Selecciona una materia")
    combo_materias.pack(pady=5)

    def actualizar_info_materia(materia):
        G = getMalla()
        info = obtener_info_materia(G, materia)
        for campo in campos:
            valor = info.get(campo, "No registrado")
            labels_info[campo].config(text=valor)

    def enviar_accion():
        materia = combo_materias.get()
        if materia == "Selecciona una materia":
            mostrar_malla_general()
            # Limpia los labels de información
            for lbl in labels_info.values():
                lbl.config(text="---")
            return
        
        # Actualiza frame de información
        actualizar_info_materia(materia)

        algoritmo = algoritmo_var.get()
        recorrido = recorrido_var.get()
        
        G = getMalla()

        if recorrido == "Post-requisitos":
            resultado = BFS_postrequisitos(G, materia) if algoritmo == "BFS" else DFS_postrequisitos(G, materia)
            ruta_img = obtener_imagen_postrequisitos(materia)
            ok = dibujarPrerequisitos(G, materia, list(resultado), True)
        else:
            resultado = BFS_prerequisitos(G, materia) if algoritmo == "BFS" else DFS_prerequisitos(G, materia)
            ruta_img = obtener_imagen_prerequisitos(materia)
            ok = dibujarPrerequisitos(G, materia, list(resultado))

        if ok and ruta_img.exists():
            cargar_y_mostrar_imagen(str(ruta_img))
        else:
            malla_canvas.delete("all")
            malla_canvas.create_text(20, 20, anchor="nw", text=f"No se pudo generar imagen para:\n{materia}", fill="black")

    def download_benchmark(materia, recorrido):
        materias = []
        tiempos = []
        
        if not materia:
            return
            
        algoritmo = algoritmo_var.get()
        
        criterio = "prerequisitos" if recorrido == "Pre-requisitos" else "postrequisitos"
        
        try:
            tiempo_list, mpm_list = sortResults(algoritmo, G, materia, criterio, 1000, 1)
            
            for tiempo_str in tiempo_list:
                tiempo = float(tiempo_str.replace("s", "").strip())
                tiempos.append(tiempo)

                materias.append([])
            
            mpm = tuple(mpm_list)
            
        except Exception as e:
            print(f"Error in benchmark: {e}")
            mpm = ("0.00000 s", "0.00000 s", "0.00000 s")
        
        os.makedirs("data", exist_ok=True)
        nombre_archivo = os.path.join("data", f"benchmark_{materia.replace(' ', '_')}.xlsx")
        
        guardar_resultados_csv(nombre_archivo, materias, tiempos, criterio, algoritmo, mpm)
        
    enviar_btn = tk.Button(btn_frame, text="Enviar", **btn_style, command=enviar_accion)
    enviar_btn.pack(fill="x", pady=5)

    descargar_btn = tk.Button(btn_frame, text="Descargar Benchmark", **btn_style,
                            command=lambda: download_benchmark(combo_materias.get(), recorrido_var.get()))
    descargar_btn.pack(fill="x", pady=5)

    planificador_btn = tk.Button(btn_frame, text="Ver Planificador", **btn_style,
                                command=abrir_ventana_planificador)
    planificador_btn.pack(fill="x", pady=5)

    def guardar_resultados_csv(nombre_archivo, materias, tiempos, criterio, algoritmo, mpm):

        resumen_data = []

        for i, tiempo in enumerate(tiempos):
            materias_intentos = materias[i] if i < len(materias) else []
            if materias_intentos and isinstance(materias_intentos, list) and len(materias_intentos) > 0:
                if isinstance(materias_intentos[0], list):
                    materias_intentos = materias_intentos[0]
            else:
                materias_intentos = []

            resumen_data.append({
                "Intento": i + 1,
                "Tiempo (s)": round(float(str(tiempo).replace("s", "").strip()), 6),
                "Criterio": criterio,
                "Algoritmo": algoritmo,
            })

        df_resumen = pd.DataFrame(resumen_data)
        df_mpm = pd.DataFrame({
            "Métrica": ["Mínimo", "Promedio", "Máximo"],
            "Tiempo (s)": [
                round(float(str(mpm[0]).replace("s", "").strip()), 6),
                round(float(str(mpm[1]).replace("s", "").strip()), 6),
                round(float(str(mpm[2]).replace("s", "").strip()), 6),
            ]
        })
        df_sistema = get_sistema_df()

        with pd.ExcelWriter(nombre_archivo) as writer:
            df_resumen.to_excel(writer, sheet_name="Resumen", index=False)
            df_mpm.to_excel(writer, sheet_name="Resumen MPM", index=False)
            df_sistema.to_excel(writer, sheet_name="Sistema", index=False)

    def get_sistema_operativo_real():
        try:
            if platform.system() == "Windows":
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
                product_name, _ = winreg.QueryValueEx(key, "ProductName")
                winreg.CloseKey(key)
                return product_name
            else:
                return platform.system()
        except:
            return platform.system()

    def get_sistema_df():
        try:
            usuario = os.getlogin()
        except:
            usuario = "Desconocido"

        info = {
            "Elemento": [
                "Sistema Operativo",
                "Versión del OS",
                "Nombre del Equipo",
                "Tipo de sistema",
                "Arquitectura",
                "Procesador",
                "Núcleos físicos",
                "Núcleos lógicos",
                "RAM Total (GB)",
                "Memoria ROM / Disco (GB)",
                "Usuario actual"
            ],
            "Valor": [
                get_sistema_operativo_real(), 
                platform.version(),
                platform.node(),
                platform.architecture()[0],
                platform.machine(),
                platform.processor(),
                psutil.cpu_count(logical=False),
                psutil.cpu_count(logical=True),
                f"{psutil.virtual_memory().total / (1024**3):.2f}",
                f"{psutil.disk_usage('/').total / (1024**3):.2f}",
                usuario
            ]
        }

        return pd.DataFrame(info)
    
    # Variables de control
    scale_factor = 0.6
    malla_img = None
    image_id = None
    drag_data = {"x": 0, "y": 0}

    # Funciones de malla
    def cargar_y_mostrar_imagen(path, reset_zoom=True):
        nonlocal malla_img, scale_factor, image_id
        ultima_ruta_img[0] = path
        try:
            img = Image.open(path)
            if reset_zoom:
                scale_factor = 0.6

            w, h = int(img.width * scale_factor), int(img.height * scale_factor)
            img = img.resize((w, h), Image.LANCZOS)

            malla_img = ImageTk.PhotoImage(img)
            malla_canvas.delete("all")
            malla_canvas.imgtk = malla_img

            # Crear imagen centrada en (0,0)
            image_id = malla_canvas.create_image(0, 0, anchor="nw", image=malla_img)
            malla_canvas.config(scrollregion=malla_canvas.bbox("all"))
            malla_canvas.current_image_path = path
        except:
            malla_canvas.delete("all")
            malla_canvas.create_text(20, 20, anchor="nw", text=f"Error cargando imagen", fill="black")

    def mostrar_malla_general():
        cargar_y_mostrar_imagen(str(malla_path))

    mostrar_malla_general()

    # --------------------
    # Zoom centrado en el cursor
    # --------------------
    def zoom(event):
        nonlocal scale_factor, malla_img, image_id

        if malla_img is None:
            return

        factor = 1.1 if (event.delta > 0 or event.num == 4) else 0.9
        new_scale = scale_factor * factor
        new_scale = max(0.2, min(new_scale, 3.0))

        # Posición del cursor sobre el canvas
        mouse_x = malla_canvas.canvasx(event.x)
        mouse_y = malla_canvas.canvasy(event.y)

        # Tamaño actual
        old_w, old_h = malla_img.width(), malla_img.height()

        # Relativo dentro de la imagen
        rel_x = (mouse_x - malla_canvas.coords(image_id)[0]) / old_w
        rel_y = (mouse_y - malla_canvas.coords(image_id)[1]) / old_h

        # Actualizar escala
        scale_factor = new_scale

        # Redibujar imagen escalada
        img = Image.open(malla_canvas.current_image_path)
        w, h = int(img.width * scale_factor), int(img.height * scale_factor)
        img = img.resize((w, h), Image.LANCZOS)
        malla_img = ImageTk.PhotoImage(img)

        malla_canvas.delete(image_id)
        image_id = malla_canvas.create_image(0, 0, anchor="nw", image=malla_img)

        # Nueva posición para que el punto del cursor quede igual
        new_x = mouse_x - rel_x * w
        new_y = mouse_y - rel_y * h
        malla_canvas.coords(image_id, new_x, new_y)

        malla_canvas.config(scrollregion=malla_canvas.bbox("all"))

    malla_canvas.bind("<MouseWheel>", zoom)
    malla_canvas.bind("<Button-4>", zoom)
    malla_canvas.bind("<Button-5>", zoom)

    # --------------------
    # Pan / Arrastrar imagen con clic izquierdo
    # --------------------
    def start_drag(event):
        drag_data["x"] = event.x
        drag_data["y"] = event.y

    def do_drag(event):
        # Diferencia de movimiento
        dx = event.x - drag_data["x"]
        dy = event.y - drag_data["y"]

        # Mover la imagen
        malla_canvas.move(image_id, dx, dy)

        # Actualizar punto de inicio
        drag_data["x"] = event.x
        drag_data["y"] = event.y

        malla_canvas.config(scrollregion=malla_canvas.bbox("all"))

    malla_canvas.bind("<ButtonPress-1>", start_drag)
    malla_canvas.bind("<B1-Motion>", do_drag)


    malla_canvas.bind("<MouseWheel>", zoom)
    malla_canvas.bind("<Button-4>", zoom)  
    malla_canvas.bind("<Button-5>", zoom)  

    perfil_ventana.logo = logo_tk if 'logo_tk' in locals() else None

def cerrar_ventana(ventana, ventana_login):
    ventana.destroy()
    ventana_login.deiconify()
