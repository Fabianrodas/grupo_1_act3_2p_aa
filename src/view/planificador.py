import tkinter as tk
from tkinter import ttk
from src.logic.planificador import planificar_carrera

def abrir_ventana_planificador():
    ventana = tk.Toplevel()
    ventana.title("Planificador de Carrera")
    ventana.geometry("1100x700")
    ventana.resizable(True, True)
    ventana.configure(bg="white")

    tk.Label(ventana, text="Planificador de Carrera", font=("Helvetica", 16, "bold"), bg="white").pack(pady=15)
    tk.Label(ventana, text="¿En cuántos años deseas terminar la carrera?", bg="white").pack(pady=5)

    opciones_anios = [str(i) for i in range(4, 8)]
    combo_anios = ttk.Combobox(ventana, values=opciones_anios, state="readonly", width=10, font=("Helvetica", 12))
    combo_anios.set(opciones_anios[0])
    combo_anios.pack(pady=10)

    # Canvas con scroll vertical
    canvas = tk.Canvas(ventana, bg="white")
    scrollbar_y = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    frame_scroll = tk.Frame(canvas, bg="white")

    frame_scroll.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_y.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar_y.pack(side="right", fill="y")

    def calcular_plan():
        for widget in frame_scroll.winfo_children():
            widget.destroy()

        anios = int(combo_anios.get())
        resultado = planificar_carrera(anios)

        # Resumen
        tk.Label(frame_scroll, text=f"Total materias: {resultado['materias_totales']}  "
                                    f"|  Periodos: {resultado['semestres_totales']}  "
                                    f"|  ≈ {resultado['materias_por_semestre']} por periodo",
                 bg="white", font=("Helvetica", 11, "italic")).grid(row=0, column=0, columnspan=2, pady=10)

        # Mostrar periodos en dos columnas
        for i, materias in enumerate(resultado['plan'], start=1):
            tipo = resultado['tipo_semestre'][i-1] if i-1 < len(resultado['tipo_semestre']) else "Ordinario"
            color_fondo = "#d7ecff" if tipo=="Ordinario" else "#ffe0b3"

            frame_periodo = tk.Frame(frame_scroll, bg=color_fondo, bd=1, relief="solid", padx=10, pady=5)
            col = 0 if (i % 2) != 0 else 1  # alterna columnas
            row = (i+1)//2
            frame_periodo.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Encabezado
            tk.Label(frame_periodo, text=f"Periodo {i} ({tipo})", 
                     font=("Helvetica", 12, "bold"), bg=color_fondo).pack(anchor="w", pady=2)

            # Materias multilinea
            materias_texto = "\n".join(materias) if materias else "(Sin materias)"
            tk.Message(frame_periodo, text=materias_texto, width=450,
                       font=("Helvetica", 11), bg=color_fondo,
                       anchor="w", justify="left").pack(anchor="w", pady=5)

    tk.Button(ventana, text="Calcular Plan", font=("Helvetica", 12, "bold"),
              bg="#7b002c", fg="white", width=18, command=calcular_plan).pack(pady=15)

    ventana.mainloop()