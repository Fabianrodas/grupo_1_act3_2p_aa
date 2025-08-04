import networkx as nx
from collections import deque
from src.utils.consts import *

def planificar_carrera(anios_objetivo: int):
    # Mapeo de años a cantidad de periodos (semestres para la GUI)
    periodos_por_anio = {
        4: 12,
        5: 15,
        6: 18,
        7: 21
    }
    periodos_totales = periodos_por_anio.get(anios_objetivo, 15)

    # Crear grafo de prerequisitos
    G = nx.DiGraph()
    for materias in SEMESTRES.values():
        for m in materias:
            G.add_node(m)
    for pre, post in RELACIONES:
        G.add_edge(pre, post)

    todas_materias = [m for materias in SEMESTRES.values() for m in materias]
    materias_totales = len(todas_materias)

    # Materias especiales
    tit1, tit2 = TITULACION_I, TITULACION_II
    practicas = [PRACTICAS_COMUNITARIAS, PRACTICAS_LABORALES]

    # Orden topológico
    try:
        orden_topologico = list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        raise ValueError("Error: Hay ciclos en los prerequisitos.")

    # Excluir Titulación I y II al inicio
    materias_base = [m for m in orden_topologico if m not in [tit1, tit2]]

    # Inicializar plan vacío
    plan = [[] for _ in range(periodos_totales)]
    cursadas = set()
    pendientes = deque(materias_base)

    # Distribución de materias en los primeros periodos
    while pendientes:
        for i in range(periodos_totales - 2):  # Últimos 2 para titulaciones
            # Materias elegibles para este periodo
            elegibles = [
                m for m in list(pendientes)
                if all(p in cursadas for p in G.predecessors(m))
            ]
            if not elegibles:
                break

            # Límite dinámico de materias por periodo
            limite = max(1, (materias_totales // periodos_totales) + 1)

            while elegibles and len(plan[i]) < limite and pendientes:
                m = elegibles.pop(0)
                plan[i].append(m)
                pendientes.remove(m)
                cursadas.add(m)

    # Insertar prácticas en la segunda mitad si hay hueco
    for materia in practicas:
        for i in range(periodos_totales // 2, periodos_totales - 2):
            limite = max(1, (materias_totales // periodos_totales) + 1)
            if len(plan[i]) < limite:
                plan[i].append(materia)
                cursadas.add(materia)
                break

    # Últimos dos periodos para Titulación I y II
    plan[-2] = [tit1]
    plan[-1] = [tit2]

    # Limpiar periodos vacíos
    plan = [p for p in plan if p]

    # Asignar tipos de periodo (cada 3er periodo extraordinario)
    tipo_periodo = []
    for idx in range(len(plan)):
        # Cada 3er periodo es extraordinario (después de 2 ordinarios)
        if (idx + 1) % 3 == 0:
            tipo_periodo.append("Extraordinario")
        else:
            tipo_periodo.append("Ordinario")

    # Validación final
    usadas = {m for periodo in plan for m in periodo}
    if len(usadas) != materias_totales:
        faltantes = [m for m in todas_materias if m not in usadas]
        raise ValueError(f"Error: Faltan materias en el plan: {faltantes}")

    materias_por_periodo = round(materias_totales / len(plan), 2)

    # Devolvemos usando las claves que espera tu GUI
    return {
        "materias_totales": materias_totales,
        "semestres_totales": len(plan),
        "materias_por_semestre": materias_por_periodo,
        "plan": plan,
        "tipo_semestre": tipo_periodo
    }
