from logic.dfs import DFS_prerequisitos
from logic.bfs import BFS_prerequisitos
from utils.malla import getMalla, dibujarMalla

# Probando getMalla y DFS_prerequisitos

G = getMalla()
targetMateria = "Desarrollo de Aplicaciones Web"
prerequisitos = DFS_prerequisitos(G, targetMateria)
print("\nPre-requisitos encontrados (DFS):")
for materia in prerequisitos:
    print("-", materia)
    
print("------------------------")

# Probando BFS_prerequisitos
targetMateria2= "Desarrollo de Aplicaciones Web"
prerequisitos2 = BFS_prerequisitos(G, targetMateria2)
print("\nPre-requisitos encontrados (BFS):")
for materia in prerequisitos2:
    print("-", materia)
# Probando dibujarMalla

dibujarMalla(G)