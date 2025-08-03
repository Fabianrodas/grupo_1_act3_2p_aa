import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from src.utils.consts import *
from pathlib import Path
import unicodedata
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import PathPatch
from matplotlib.path import Path as Path2
import textwrap
import numpy as np

def normaliza_nombre(nombre):
    # Elimina tildes y reemplaza espacios por "_"
    nombre = unicodedata.normalize("NFD", nombre)
    nombre = nombre.encode("ascii", "ignore").decode("utf-8")
    return nombre.replace(" ", "_")

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

def dibujarMalla(G, filename="malla.png"):
    fig, ax = plt.subplots(figsize=(13, 8))  # Siempre igual tamaño
    try:
        columnas = max(len(materias) for materias in SEMESTRES.values())
        espacio_x = 4.8
        espacio_y = 2.5
        pos = {}
        for nivel, materias in SEMESTRES.items():
            offset = (columnas - len(materias)) / 2
            for i, materia in enumerate(materias):
                pos[materia] = ((i + offset) * espacio_x, -nivel * espacio_y)
        nx.draw_networkx_edges(
            G, pos, arrows=True, arrowstyle='-', connectionstyle='arc3,rad=0.0',
            width=0, edge_color="black", ax=ax
        )

        LEVEL_X_NODE = 4.8
        LEVEL_Y_NODE = 2.5
        for relations in G.edges():
            po = np.array(pos[relations[0]])
            pi = np.array(pos[relations[1]])
            current_y = -LEVEL_Y_NODE/2 if po[1] != pi[1] else 0
            current_x = 0
            verts = []
            verts.append(po)
            
            if(po[1] != pi[1]):
                verts.append(po + np.array([current_x, current_y]))

            delta_x = round(-(po[0] + current_x - pi[0]),1)
            delta_y = round(-(po[1] + current_y - pi[1]),1)
            #and ((round(po[0] + current_x - pi[0],1) != LEVEL_X_NODE/2 or round(po[0] + current_x - pi[0],1) != -LEVEL_X_NODE/2) and po[0] + current_y < pi[0] )):

            while(delta_x != 0 or delta_y != 0):

                if(delta_x > 25 or delta_y > 25):
                    break

                delta_x = round(-(po[0] + current_x - pi[0]),1)
                delta_y = round(-(po[1] + current_y - pi[1]),1)

                if(po[1] + current_y != pi[1]):
                    if((round(po[0] + current_x - pi[0],2) == LEVEL_X_NODE/2 or round(po[0] + current_x - pi[0],2) == -LEVEL_X_NODE/2) and po[1] < pi[1]):
                        current_y += LEVEL_Y_NODE/2
                    else:
                        if(round(-((po[0] + current_x) -  pi[0]), 1) < 0):
                            current_x += -LEVEL_X_NODE/2
                        elif(round(-((po[0] + current_x) - pi[0]), 1) > 0):
                            current_x += LEVEL_X_NODE/2
                        elif(round(-((po[1] + current_y) - pi[1]), 1) > 0):
                            current_y += LEVEL_Y_NODE/2
                        else:
                            current_y += -LEVEL_Y_NODE/2
                else:
                    if((round(po[0] + current_x - pi[0],1) >= -4.8 and po[0] < pi[0])  or (round(po[0] + current_x - pi[0],1) <= 4.8 and po[0] > pi[0])):
                        if(round(-((po[0] + current_x) - pi[0]), 1) < 0):
                            current_x += -LEVEL_X_NODE/2
                        else:
                            current_x += LEVEL_X_NODE/2
                    else:
                        current_y += -LEVEL_Y_NODE/2
                if(round(po[0] + current_x,1) == round(pi[0],1) and round(po[1] + current_y,1) == round(pi[1],1)):
                    break
                verts.append(po + np.array([current_x, current_y]))

            verts.append(pi)

            codes = [Path2.MOVETO] + [Path2.LINETO] * (len(verts) - 1)
            path = Path2(verts, codes)
            arrow = FancyArrowPatch(
                path=path,
                arrowstyle='->',
                color='black',
                lw=1,
                mutation_scale=15
            )
            ax.add_patch(arrow)


        for node, (x, y) in pos.items():
            color = COLOR_NODOS.get(node, "#a7caf7")
            rect = patches.FancyBboxPatch(
                (x - 1.25, y - 0.6), 2.5, 1.2,
                boxstyle="round,pad=0.02",
                linewidth=1, edgecolor="black", facecolor=color, zorder=1
            )
            ax.add_patch(rect)
            label = wrap_label(f"{node}\n({HORAS.get(node, '')})", width=20)
            ax.text(x, y, label, ha="center", va="center", fontsize=8, weight="bold", zorder=2)
        ax.set_axis_off()
        plt.tight_layout()
        plt.savefig(filename, dpi=100, bbox_inches="tight")
        plt.close(fig)
        print(f"Imagen exportada como '{filename}'")
        return True
    except Exception as e:
        plt.close(fig)
        print(f"Error generando malla: {e}")
        return False

def dibujarPrerequisitos(G, materia_principal, materias_resaltadas=None, filename=None):
    # Usar nombre normalizado para archivo
    if not materia_principal or materia_principal not in G.nodes:
        print(f"No se pudo generar imagen para: {materia_principal}")
        return False
    nombre_img = normaliza_nombre(materia_principal)
    if filename is None:
        filename = f"prerequsitos_{nombre_img}.png"

    # Calcular posiciones igual que en la malla general
    fig, ax = plt.subplots(figsize=(13, 8))  # Mantener tamaño consistente
    try:
        columnas = max(len(materias) for materias in SEMESTRES.values())
        espacio_x = 4.8
        espacio_y = 2.5
        pos = {}
        niveles_totales = len(SEMESTRES)
        for nivel, materias in SEMESTRES.items():
            offset_x = (columnas - len(materias)) / 2
            for i, materia in enumerate(materias):
                x = (i + offset_x) * espacio_x
                y = -(nivel) * espacio_y
                pos[materia] = (x, y)
        # Determinar el conjunto de nodos a resaltar
        materias_resaltadas = set(materias_resaltadas) if materias_resaltadas else set()
        nodos_marcados = materias_resaltadas | {materia_principal}

        # Edges a dibujar
        edges_to_draw = [
            (u, v) for u, v in G.edges()
            if u in nodos_marcados and v in nodos_marcados
        ]
        nx.draw_networkx_edges(
            G, pos,
            edgelist=edges_to_draw,
            arrows=True,
            arrowstyle='-|>',
            width=0,
            edge_color="red",
            ax=ax
        )

        
        LEVEL_X_NODE = 4.8
        LEVEL_Y_NODE = 2.5
        for relations in edges_to_draw:
            po = np.array(pos[relations[0]])
            pi = np.array(pos[relations[1]])
            current_y = -LEVEL_Y_NODE/2 if po[1] != pi[1] else 0
            current_x = 0
            verts = []
            verts.append(po)
            
            if(po[1] != pi[1]):
                verts.append(po + np.array([current_x, current_y]))

            delta_x = round(-(po[0] + current_x - pi[0]),1)
            delta_y = round(-(po[1] + current_y - pi[1]),1)
            #and ((round(po[0] + current_x - pi[0],1) != LEVEL_X_NODE/2 or round(po[0] + current_x - pi[0],1) != -LEVEL_X_NODE/2) and po[0] + current_y < pi[0] )):

            while(delta_x != 0 or delta_y != 0):

                if(delta_x > 25 or delta_y > 25):
                    break

                delta_x = round(-(po[0] + current_x - pi[0]),1)
                delta_y = round(-(po[1] + current_y - pi[1]),1)

                if(po[1] + current_y != pi[1]):
                    if((round(po[0] + current_x - pi[0],2) == LEVEL_X_NODE/2 or round(po[0] + current_x - pi[0],2) == -LEVEL_X_NODE/2) and po[1] < pi[1]):
                        current_y += LEVEL_Y_NODE/2
                    else:
                        if(round(-((po[0] + current_x) -  pi[0]), 1) < 0):
                            current_x += -LEVEL_X_NODE/2
                        elif(round(-((po[0] + current_x) - pi[0]), 1) > 0):
                            current_x += LEVEL_X_NODE/2
                        elif(round(-((po[1] + current_y) - pi[1]), 1) > 0):
                            current_y += LEVEL_Y_NODE/2
                        else:
                            current_y += -LEVEL_Y_NODE/2
                else:
                    if((round(po[0] + current_x - pi[0],1) >= -4.8 and po[0] < pi[0])  or (round(po[0] + current_x - pi[0],1) <= 4.8 and po[0] > pi[0])):
                        if(round(-((po[0] + current_x) - pi[0]), 1) < 0):
                            current_x += -LEVEL_X_NODE/2
                        else:
                            current_x += LEVEL_X_NODE/2
                    else:
                        current_y += -LEVEL_Y_NODE/2
                if(round(po[0] + current_x,1) == round(pi[0],1) and round(po[1] + current_y,1) == round(pi[1],1)):
                    break
                verts.append(po + np.array([current_x, current_y]))

            verts.append(pi)

            codes = [Path2.MOVETO] + [Path2.LINETO] * (len(verts) - 1)
            path = Path2(verts, codes)
            arrow = FancyArrowPatch(
                path=path,
                arrowstyle='->',
                color='black',
                lw=1,
                mutation_scale=15
            )
            ax.add_patch(arrow)


        # Nodos (resaltados y no resaltados)
        for node, (x, y) in pos.items():
            if node == materia_principal:
                facecolor = "#f4a261"  # Naranja principal
                edgecolor = "black"
                textcolor = "black"
            elif node in materias_resaltadas:
                facecolor = "#ffe699"  # Amarillo prerequisitos
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
            label = wrap_label(f"{node}\n({HORAS.get(node, '')})", width=20)
            ax.text(x, y, label, ha="center", va="center", fontsize=8, weight="bold", color=textcolor, zorder=2)
        ax.set_axis_off()
        plt.tight_layout()
        plt.savefig(filename, dpi=100, bbox_inches="tight")
        plt.close(fig)
        print(f"Imagen exportada como '{filename}'")
        return True
    except Exception as e:
        plt.close(fig)
        print(f"No se pudo generar imagen para: {materia_principal}\nError: {e}")
        return False
