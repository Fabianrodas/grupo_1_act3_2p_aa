# Proyecto Malla Curricular

Este proyecto fue creado con el objetivo de mostrar comparativas entre dos algoritmos existentes en los grafos: BFS y DFS. Es un programa sencillo que simula el portal de servicios de la Universidad de Especialidades Espíritu Santo (UEES), en el cual podrás ver la malla actual de Ciencias de la Computación y observar los distintos prerrequisitos/postrequisitos de cualquier materia, para ayudarte a conocer qué materias deberías cursar o cursarás siguiendo ese flujo.

Este programa se logró con ayuda de grafos, donde cada nodo representa una materia y sus relaciones el flujo que sigue esta materia con respecto a otras. Para ayudar al usuario a conocer el flujo que recibe o da una materia de la universidad, fue necesaria la inclusión de 2 algoritmos: DFS y BFS, los cuales logran encontrar los caminos posibles, dando a conocer el conjunto de materias (nodos) que están conectadas a la materia que se escogió.

## Preview del programa

<img src="https://i.imgur.com/DZRYUAp.png" height=300>
<img src="https://i.imgur.com/6tog9jg.png" height=300>
<img src="https://i.imgur.com/CTBRvVn.png" height=300>
<img src="https://i.imgur.com/q6kxe0h.png" height=300>

# Librerías Usadas

| Librería |Documentación|Descripción|Versiódn |
|----------|-------------|-----------|---------|
|Matplotlib|<a href="https://matplotlib.org/"> ![matplotlib.png](https://matplotlib.org/_static/logo_light.svg)</a> |Usado para la que tenga una UI interactiva y animada. | 3.10.5 
|NetworkX          |<a href="https://networkx.org/">  ![matplotlib.png](https://networkx.org/_static/networkx_logo.svg)</a> |Librería usada para mostrar grafos de manera visual. | 3.5
|Pandas          |<a href="https://networkx.org/">  ![matplotlib.png](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/800px-Pandas_logo.svg.png)</a> |Librería usada para convertir los datos en archivos .xls para crear las gráficas posteriormente. | 2.1.3
|Numpy          |<a href="https://networkx.org/">  ![matplotlib.png](https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/NumPy_logo_2020.svg/1200px-NumPy_logo_2020.svg.png)</a> |Librería usada para colocar ordenadamente los nodos (materias) dentro de la malla curricular | 2.3.1 
|Tkinter          |<a href="https://networkx.org/">  ![matplotlib.png](https://ucarecdn.com/58fe6c9f-2b0f-455c-932a-cbcb7a72b224/-/resize/1050/)</a> |Librería usada para realizar interfaces gráficas | 1.5.7 

# Instalación

Para la instalación y el correcto uso del programa, primero clone el repositorio usando el comando `git clone <link-del-repositorio>`, si ya lo tiene clonado use un `git fetch` y luego un `git pull` por si existen cambios dentro del mismo.

Ahora deberá de obtener todos las librerías que usamos en el proyecto, lo recomendable es que use el comando `pip install -r requirements.txt` desde la raíz del proyecto para instalar todas las librerías usadas en la misma. 

> Nota: A veces pueden ocurrir errores, si te pasan errores al ejecutar, trata de crear un entorno virtual y luego vuelve a instalar las dependencias del proyecto.

Una vez instaladas las dependencias del proyecto, dirigete al archivo `app.py` y ejecutalo, con esto podrás ver la interfaz. Si simplemente quieres descargar la **malla principal** dirigete al archivo `malla.py` y ejecutalo, esto te descargará un **malla.png** junto a un ejemplo de los prerequisitos de una materia como prueba.

# Notas a tener en cuenta

Si deseas agregar más materias o disminuirlas, puedes irte al archivo `consts.py`, allí encontrarás muchas constantes que usamos en el proyecto, destacando las de `SEMESTRES` y `RELACIONES`, las cuales albergan todos los nodos a usar en el proyecto que en su defecto deberían de ser 40.

> Nota: Nada garantiza que al modificar el archivo de `consts.py` puedas dañar la ejecución del proyecto, es por eso que seas consciente de lo que modificas y en un caso de corrupción del proyecto, vuelvas a clonarlo.

También es importante aclarar que las gráficas sobre el flujo que siguen las materias pueden no verse del todo claro con respecto a las flechas que deberían de tener, pero esto se debe a que siendo python que es un lenguaje destacado por el analisis, graficar las flechas se hizo una tarea muy dificil.

## 👥 Contribuidores

Este proyecto fue realizado gracias a la contribución de las siguientes personas:

- Dylan Drouet
- Fabian Rodas
- Luis Goncalves 
- Andrea Torres
