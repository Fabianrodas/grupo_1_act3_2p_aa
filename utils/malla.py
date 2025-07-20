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
        "Organización y Arquitectura de Computadores", "Redes y Comunicaciones", "Base de Datos II", "Programación Orientada a Objetos", "Comunicación e Imagen Profesional",
        # Año 3
        # Quinto Semestre
        "Sistemas Operativos", "Diseño de Software", "Lenguajes de Programación", "Estructura de Datos", "Desarrollo Sostenible",
        # Sexto Semestre
        "Sistemas Distribuidos", "Interacción Hombre-Máquina", "Desarrollo de Aplicaciones Web", "Análisis de Algoritmos", "Liderazgo, Emprendimiento e Innovación",
        # Año 4
        # Septimo Semestre
        "Procesamiento Masivo de Datos", "Ingeniería de Software I", "Sistemas Inteligentes", "Prácticas de Servicio Comunitario", "Proyecto de Titulación I"
        # Octavo Semestre
        "Ethical Hacking", "Ingeniería de Software II", "Fundamentos de Computación Forense", "Prácticas Laborales", "Proyecto de Titulación II"
    ]

    malla.add_nodes_from(materias)
    
    relaciones = [
        # Primer Semestre
        ("Matemáticas I", "Matemáticas II"), ("Física I", "Física II"), ("Álgebra Lineal", "Probabilidad y Estadística"), ("Computación y Sociedad", "Matemáticas Discretas"),
        # Segundo Semestre
        ("Matemáticas II", "Matemáticas III"), ("Física II", "Lógica Digital"), ("Probabilidad y Estadística", "Lógica Digital"), ("Matemáticas Discretas", "Fundamentos de Programación"), ("Tecnologías Disruptivas", "Base de Datos I"), ("Tecnologías Disruptivas", "Fundamentos de Programación"),
        # Tercer Semestre
        ("Matemáticas III", "Redes y Comunicaciones"), ("Lógica Digital", "Organización y Arquitectura de Computadoras"), ("Lógica Digital", "Redes y Comunicaciones"), ("Base de Datos I", "Base de Datos II"), ("Fundamentos de Programación", "Base de Datos I"), ("Fundamentos de Programación", "Programación Orientada a Objetos"),
        # Cuarto Semestre
        ("Organización y Arquitectura de Computadores", "Sistemas Operativos"), ("Redes y Comunicaciones", "Sistemas Operativos"), ("Base de Datos II", "Desarrollo de Aplicaciones Web"), ("Programación Orientada a Objetos", "Sistemas Operativos"), ("Programación Orientada a Objetos", "Diseño de Software"), ("Programación Orientada a Objetos", "Lenguajes de Programación"), ("Programación Orientada a Objetos", "Estructura de Datos"), 
        # Quinto Semestre
        ("Sistemas Operativos", "Sistemas Distribuidos"), ("Diseño de Software", "Desarrollo de Aplicaciones Web"), ("Lenguajes de Programación", "Diseño de Software"), ("Lenguajes de Programación", "Desarrollo de Aplicaciones Web"), ("Estructura de Datos", "Lenguajes de Programación"), ("Estructura de Datos", "Análisis de Algoritmos"),
        # Sexto Semestre
        ("Sistemas Distribuidos", "Procesamiento Masivo de Datos"), ("Sistemas Distribuidos", "Sistemas Inteligentes"), ("Interacción Hombre Máquina", "Ingeniería de Software I"), ("Desarrollo de Aplicaciones Web", "Interacción Hombre Máquina"), ("Desarrollo de Aplicaciones Web", "Sistemas Inteligentes"), ("Análisis de Algoritmos", "Sistemas Inteligentes"),
        # Séptimo Semestre
        ("Procesamiento Masivo de Datos", "Ethical Hacking"), ("Procesamiento Masivo de Datos", "Proyecto de Titulación I"), ("Procesamiento Masivo de Datos", "Proyecto de Titulación II"), ("Ingeniería de Software I", "Ingeniería de Software II"), ("Sistemas Inteligentes", "Fundamentos de Computación Forense"), ("Sistemas Inteligentes", "Proyecto de Titulación I"), ("Sistemas Inteligentes", "Proyecto de Titulación II"), ("Proyecto de Titulación I", "Proyecto de Titulación II"),
        # Octavo Semestre
        ("Ethical Hacking", "Proyecto de Titulación I"), ("Ethical Hacking", "Proyecto de Titulación II"), ("Ingeniería de Software II", "Proyecto de Titulación I"), ("Ingeniería de Software II", "Proyecto de Titulación II"), ("Fundamentos de Computación Forense", "Proyecto de Titulación I"), ("Fundamentos de Computación Forense", "Proyecto de Titulación II")
    ]

    malla.add_edges_from(relaciones)
    
    return malla
