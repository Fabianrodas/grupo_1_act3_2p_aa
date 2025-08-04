def DFS_prerequisitos_interno(grafo, materia, visitados=None):
    if visitados is None:
        visitados = set()
    
    visitados.add(materia)
    for prerequisito in grafo.predecessors(materia):
        if prerequisito not in visitados:
            print(f"Visitando materia: {prerequisito}")
            DFS_prerequisitos_interno(grafo, prerequisito, visitados)
    
    return visitados

def DFS_prerequisitos(grafo, materia, visitados=None):
    resultado = DFS_prerequisitos_interno(grafo, materia)
    resultado.remove(materia)
    return resultado

def DFS_postrequisitos_interno(grafo, materia, visitados=None):
    if visitados is None:
        visitados = set()
    
    visitados.add(materia)
    for postrequisito in grafo.successors(materia):
        if postrequisito not in visitados:
            print(f"Visitando materia: {postrequisito}")
            DFS_postrequisitos_interno(grafo, postrequisito, visitados)
    
    return visitados

def DFS_postrequisitos(grafo, materia):
    resultado = DFS_postrequisitos_interno(grafo, materia)
    resultado.remove(materia)
    return resultado