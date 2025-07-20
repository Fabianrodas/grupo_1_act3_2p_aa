import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from consts import *
import textwrap

def getMalla():
    malla = nx.DiGraph()
    for materias in SEMESTRES.values():
        malla.add_nodes_from(materias)
    malla.add_edges_from(RELACIONES)
    
    return malla

def wrap_label(text, width=20):
    return "\n".join(textwrap.wrap(text, width=width))

def dibujarMalla(G):
    pos = {}
    columnas = max(len(materias) for materias in SEMESTRES.values())
    espacio_x = 4.5
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
    plt.show()
    
dibujarMalla(getMalla())