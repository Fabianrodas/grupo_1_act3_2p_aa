from collections import deque

def BFS_prerequisitos_interno(grafo, materia, visitados=None):
    if visitados is None:
        visitados = set()
    
    cola=deque()
    cola.append(materia)
    visitados.add(materia)

    while cola:
        actual = cola.popleft()
        for preriquisito in grafo.predecessors(actual):
            if preriquisito not in visitados:
                print(f"Visitando materia: {preriquisito}")
                visitados.add(preriquisito)
                cola.append(preriquisito)

    return visitados

def BFS_prerequisitos(grafo, materia, visitados=None):
    resultado =BFS_prerequisitos_interno(grafo, materia)
    resultado.remove(materia)
    return resultado
    

    