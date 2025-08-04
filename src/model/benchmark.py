from src.logic.dfs import DFS_prerequisitos
from src.logic.bfs import BFS_prerequisitos
from src.logic.dfs import DFS_postrequisitos
from src.logic.bfs import BFS_postrequisitos
import timeit

def BFS(G, targetMateria, criterio):
    if(criterio == "prerequisitos"):
        BFS_prerequisitos(G,targetMateria)
    elif(criterio == "postrequisitos"):
        BFS_postrequisitos(G,targetMateria)
        
def DFS(G, targetMateria, criterio):
    if(criterio == "prerequisitos"):
        DFS_prerequisitos(G,targetMateria)
    elif(criterio == "postrequisitos"):
        DFS_postrequisitos(G,targetMateria)


def sortResults(str, G, targetMateria, criterio, reps, num):
    if(str == "BFS"):   
        times = timeit.repeat(stmt=lambda: BFS(G, targetMateria, criterio), repeat=reps, number=num)
    elif(str == "DFS"):
        times = timeit.repeat(stmt=lambda: DFS(G, targetMateria, criterio), repeat=reps, number=num)

    tiempos = []
    mpm = []
    for i,t in enumerate(times,1):
        tiempos.append(f"{t:.5f} s")  
    mpm.append(f"{min(times):.5f} s")
    mpm.append(f"{sum(times)/len(times):.5f} s")
    mpm.append(f"{max(times):.5f} s")
    
    return tiempos, mpm
