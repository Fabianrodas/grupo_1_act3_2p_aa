import networkx as nx
import matplotlib.pyplot as plt

def getMalla():
    malla = nx.DiGraph()

    materias = [
        # Año 1
        # Primer Semestre
        "Matemáticas I", "Física I", "Álgebra Lineal", "Computación y Sociedad", "Ética",
        # Segundo Semestre
        "Matemáticas II", "Física II", "Probabilidad y Estadística", "Matemáticas Discretas", "Tecnologías Disruptivas",
        # Año 2
        # Tercer Semestre
        "Matemáticas III", "Lógica Digital", "Base de Datos I", "Fundamentos de Programación", "Desarrollo Humano",
        # Cuarto Semestre
        "Organización y Arquitectura de Computadoras", "Redes y Comunicaciones", "Base de Datos II", "Programación Orientada a Objetos", "Comunicación e Imagen Profesional",
        # Año 3
        # Quinto Semestre
        "Sistemas Operativos", "Diseño de Software", "Lenguajes de Programación", "Estructura de Datos", "Desarrollo Sostenible",
        # Sexto Semestre
        "Sistemas Distribuidos", "Interacción Hombre-Máquina", "Desarrollo y Aplicaciones Web", "Análisis de Algoritmos", "Liderazgo, Emprendimiento e Innovación",
        # Año 4
        # Septimo Semestre
        "Procesamiento Masivo de Datos", "Ingeniería de Software I", "Sistemas Inteligentes", "Prácticas de Servicio Comunitario", "Proyecto de Titulación I"
        # Octavo Semestre
        "Ethical Hacking", "Ingeniería de Software II", "Fundamentos de Computación Forense", "Prácticas Laborales", "Proyecto de Titulación II"
    ]

    malla.add_nodes_from(materias)
    
    return malla
