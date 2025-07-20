import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from .consts import *
import textwrap

SEMESTRES = {
    1: [MATEMATICAS_I, FISICA_I, ALGEBRA_LINEAL, COMPUTACION_SOCIEDAD, ETICA],
    2: [MATEMATICAS_II, FISICA_II, PROBABILIDAD_ESTADISTICA, MATEMATICAS_DISCRETAS, TECNOLOGIAS_DISRUPTIVAS],
    3: [MATEMATICAS_III, LOGICA_DIGITAL, BASE_DATOS_I, FUNDAMENTOS_PROGRAMACION, DESARROLLO_HUMANO],
    4: [OAC, REDES_COMUNICACIONES, BASE_DATOS_II, POO, COMUNICACION_PROFESIONAL],
    5: [SISTEMAS_OPERATIVOS, DDS, LENGUAJES_PROGRAMACION, ESTRUCTURA_DATOS, DESARROLLO_SOSTENIBLE],
    6: [SISTEMAS_DISTRIBUIDAS, INTERACCION_HM, DESARROLLO_WEB, ANALISIS_ALGORITMOS, LIDERAZGO_EMPRENDIMIENTO],
    7: [PROCESAMIENTO_DATOS, INGENIERIA_SOFTWARE_I, SISTEMAS_INTELIGENTES, PRACTICAS_COMUNITARIAS, TITULACION_I],
    8: [ETHICAL_HACKING, INGENIERIA_SOFTWARE_II, FUNDAMENTOS_FORENSES, PRACTICAS_LABORALES, TITULACION_II]
}

RELACIONES = [
    # Primer Semestre
    (MATEMATICAS_I, MATEMATICAS_II), (FISICA_I, FISICA_II), (ALGEBRA_LINEAL, PROBABILIDAD_ESTADISTICA), (COMPUTACION_SOCIEDAD, MATEMATICAS_DISCRETAS),
    # Segundo Semestre
    (MATEMATICAS_II, MATEMATICAS_III), (FISICA_II, LOGICA_DIGITAL), (PROBABILIDAD_ESTADISTICA, LOGICA_DIGITAL), (MATEMATICAS_DISCRETAS, FUNDAMENTOS_PROGRAMACION), (TECNOLOGIAS_DISRUPTIVAS, BASE_DATOS_I), (TECNOLOGIAS_DISRUPTIVAS, FUNDAMENTOS_PROGRAMACION),
    # Tercer Semestre
    (MATEMATICAS_III, REDES_COMUNICACIONES), (LOGICA_DIGITAL, OAC), (LOGICA_DIGITAL, REDES_COMUNICACIONES), (BASE_DATOS_I, BASE_DATOS_II), (FUNDAMENTOS_PROGRAMACION, BASE_DATOS_I), (FUNDAMENTOS_PROGRAMACION, POO),
    # Cuarto Semestre
    (OAC, SISTEMAS_OPERATIVOS), (REDES_COMUNICACIONES, SISTEMAS_OPERATIVOS), (BASE_DATOS_II, DESARROLLO_WEB), (POO, SISTEMAS_OPERATIVOS), (POO, DDS), (POO, LENGUAJES_PROGRAMACION), (POO, ESTRUCTURA_DATOS), 
    # Quinto Semestre
    (SISTEMAS_OPERATIVOS, SISTEMAS_DISTRIBUIDAS), (DDS, DESARROLLO_WEB), (LENGUAJES_PROGRAMACION, DDS), (LENGUAJES_PROGRAMACION, DESARROLLO_WEB), (ESTRUCTURA_DATOS, LENGUAJES_PROGRAMACION), (ESTRUCTURA_DATOS, ANALISIS_ALGORITMOS),
    # Sexto Semestre
    (SISTEMAS_DISTRIBUIDAS, PROCESAMIENTO_DATOS), (SISTEMAS_DISTRIBUIDAS, SISTEMAS_INTELIGENTES), (INTERACCION_HM, INGENIERIA_SOFTWARE_I), (DESARROLLO_WEB, INTERACCION_HM), (DESARROLLO_WEB, SISTEMAS_INTELIGENTES), (ANALISIS_ALGORITMOS, SISTEMAS_INTELIGENTES),
    # Séptimo Semestre
    (PROCESAMIENTO_DATOS, ETHICAL_HACKING), (PROCESAMIENTO_DATOS, TITULACION_I), (PROCESAMIENTO_DATOS, TITULACION_II), (INGENIERIA_SOFTWARE_I, INGENIERIA_SOFTWARE_II), (SISTEMAS_INTELIGENTES, FUNDAMENTOS_FORENSES), (SISTEMAS_INTELIGENTES, TITULACION_I), (SISTEMAS_INTELIGENTES, TITULACION_II), (TITULACION_I, TITULACION_II),
    # Octavo Semestre
    (ETHICAL_HACKING, TITULACION_I), (ETHICAL_HACKING, TITULACION_II), (INGENIERIA_SOFTWARE_II, TITULACION_I), (INGENIERIA_SOFTWARE_II, TITULACION_II), (FUNDAMENTOS_FORENSES, TITULACION_I), (FUNDAMENTOS_FORENSES, TITULACION_II)
]

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
    labels_envueltos = {nodo: wrap_label(nodo, width=20) for nodo in G.nodes}

    # TAMAÑO DE LA FIGURA
    fig, ax = plt.subplots(figsize=(11, 7))
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
        rect = patches.FancyBboxPatch(
            (x - 1.25, y - 0.6), 2.5, 1.2,
            boxstyle="round,pad=0.02",
            linewidth=1, edgecolor="black", facecolor="skyblue", zorder=1
        )
        ax.add_patch(rect)

    # ETIQUETAS DE MATERIAS
    for node, (x, y) in pos.items():
        ax.text(
            x, y, labels_envueltos[node],
            ha="center", va="center", fontsize=7, weight="bold", zorder=2
        )

    ax.set_title("Malla Ing. Computación", fontsize=15)
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()
    
dibujarMalla(getMalla())