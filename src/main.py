from logic.dfs import DFS_prerequisitos
from logic.bfs import BFS_prerequisitos
from utils.malla import getMalla, dibujarMalla, dibujarPrerequisitos

# Probando getMalla y DFS_prerequisitos

G = getMalla()

# Probando BFS_prerequisitos
targetMateria2= "Ingeniería de Software II"
prerequisitos2 = BFS_prerequisitos(G, targetMateria2)

dibujarMalla(G)
dibujarPrerequisitos(G, targetMateria2, prerequisitos2)