from logic.dfs import DFS_prerequisitos
from utils.malla import getMalla, dibujarMalla

# Probando getMalla y DFS_prerequisitos

G = getMalla()
targetMateria = "Desarrollo de Aplicaciones Web"
prerequisitos = DFS_prerequisitos(G, targetMateria)
print("\nPre-requisitos encontrados:")
for materia in prerequisitos:
    print("-", materia)
    
# Probando dibujarMalla

dibujarMalla(G)