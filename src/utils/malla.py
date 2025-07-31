import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.consts import *
import textwrap
from pathlib import Path

def getMalla():
    malla = nx.DiGraph()

    for materias in SEMESTRES.values():
        for materia in materias:
            atributos = Materias_Info.get(materia, {})
            malla.add_node(materia, **atributos)

    malla.add_edges_from(RELACIONES)
    return malla

def obtener_info_materia(grafo, nombre_materia):
    if nombre_materia in grafo.nodes:
        atributos = grafo.nodes[nombre_materia]
        return {
            "Materia": nombre_materia,
            "Código": atributos.get("codigo", "No registrado"),
            "Profesor": atributos.get("profesor", "No registrado"),
            "Horario": atributos.get("horario", "No registrado")
        }
    else:
        return {"Error": "Materia no encontrada"}

def wrap_label(text, width=20):
    return "\n".join(textwrap.wrap(text, width=width))

def dibujarMalla(G):
    if Path("malla.png").exists():
        print("La imagen 'malla.png' ya existe.")
        return
    
    pos = {}
    columnas = max(len(materias) for materias in SEMESTRES.values())
    espacio_x = 4.8
    espacio_y = 2.5

    for nivel, materias in SEMESTRES.items():
        offset = (columnas - len(materias)) / 2
        for i, materia in enumerate(materias):
            pos[materia] = ((i + offset) * espacio_x, -nivel * espacio_y)

    # TAMAÑO DE LA FIGURA
    fig, ax = plt.subplots(figsize=(12, 8))
    try:
        manager = plt.get_current_fig_manager()
        manager.window.setFixedSize(1300, 900)
    except:
        pass

    # RELACIONES (LINEAS ENTRE NODOS)
    nx.draw_networkx_edges(
        G, pos, arrows=True, arrowstyle='-', connectionstyle='arc3,rad=0.0',
        width=1, edge_color="black", ax=ax
    )

    # RECTANGULOS DE MATERIAS
    for node, (x, y) in pos.items():
        color = COLOR_NODOS.get(node, "#cccccc")
        rect = patches.FancyBboxPatch(
            (x - 1.25, y - 0.6), 2.5, 1.2,
            boxstyle="round,pad=0.02",
            linewidth=1, edgecolor="black", facecolor=color, zorder=1
        )
        ax.add_patch(rect)

        label = wrap_label(node, width=20) + f"\n({HORAS.get(node, '')})"
        
        # ETIQUETAS DE MATERIAS
        ax.text(
            x, y, label,
            ha="center", va="center", fontsize=7, weight="bold", zorder=2
        )

    ax.set_axis_off()
    plt.tight_layout()
    
    plt.savefig(f"malla.png", dpi=300, bbox_inches="tight")
    print("Imagen exportada como 'malla_curricular.png'")

def dibujarPrerequisitos(G, materia_principal=None, materias_resaltadas=None):
    if Path(f"prerequsitos_{materia_principal}.png").exists():
        print(f"La imagen 'prerequsitos_{materia_principal}.png' ya existe.")
        return
    
    pos = {}
    columnas = max(len(materias) for materias in SEMESTRES.values())
    espacio_x = 4.5
    espacio_y = 2.5

    # Preparar conjunto de materias marcadas
    materias_resaltadas = set(materias_resaltadas) if materias_resaltadas else set()
    nodos_marcados = materias_resaltadas.union({materia_principal}) if materia_principal else materias_resaltadas

    # Posicionar nodos centrados
    niveles_totales = len(SEMESTRES)
    for nivel, materias in SEMESTRES.items():
        offset_x = (columnas - len(materias)) / 2
        for i, materia in enumerate(materias):
            x = (i + offset_x) * espacio_x
            y = -(nivel - (niveles_totales - 1) / 2) * espacio_y  
            pos[materia] = (x, y)

    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 7))

    # Dibujar solo relaciones relevantes (en rojo)
    edges_to_draw = [
        (u, v) for u, v in G.edges()
        if u in nodos_marcados and v in nodos_marcados
    ]

    nx.draw_networkx_edges(
        G, pos,
        edgelist=edges_to_draw,
        arrows=True,
        arrowstyle='-|>',
        width=2,
        edge_color="red",
        ax=ax
    )

    # Dibujar nodos
    for node, (x, y) in pos.items():
        if node == materia_principal:
            facecolor = "#f4a261" 
            edgecolor = "black"
            textcolor = "black"
        elif node in materias_resaltadas:
            facecolor = "#ffe699"
            edgecolor = "black"
            textcolor = "black"
        else:
            facecolor = "white"
            edgecolor = "white"
            textcolor = "#dddddd"

        rect = patches.FancyBboxPatch(
            (x - 1.25, y - 0.6), 2.5, 1.2,
            boxstyle="round,pad=0.02",
            linewidth=1.3,
            edgecolor=edgecolor,
            facecolor=facecolor,
            zorder=1
        )
        ax.add_patch(rect)

        label = wrap_label(node, width=20) + f"\n({HORAS.get(node, '')})"

        ax.text(
            x, y, label,
            ha="center", va="center", fontsize=7,
            weight="bold", color=textcolor, zorder=2
        )

    ax.set_axis_off()
    plt.tight_layout()

    plt.savefig(f"prerequsitos_{materia_principal}.png", dpi=300, bbox_inches="tight")
    print("Imagen exportada como 'malla_curricular.png'")