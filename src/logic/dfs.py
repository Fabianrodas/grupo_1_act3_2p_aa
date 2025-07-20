import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.malla import getMalla

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

G = getMalla()
targetMateria = "Base de Datos I"
prerequisitos = DFS_prerequisitos(G, targetMateria)
print("\nPre-requisitos encontrados:")
for materia in prerequisitos:
    print("-", materia)