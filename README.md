# Sudoku

Juego de Sudoku clásico (tablero de 9x9) en Python. Permite generar tableros con distintos niveles de dificultad, jugar validando cada jugada y resolver el tablero automáticamente.

## Desarrolladores del proyecto
- [Nombre 1]
- [Nombre 2]
- [Nombre 3]

## Especificaciones del proyecto
El juego genera un tablero válido con solución única, oculta una cantidad de casillas según la dificultad elegida y valida cada número que el jugador ingresa según las reglas del Sudoku. Utiliza únicamente módulos nativos de Python, por lo que no requiere instalar dependencias externas.

### Reglas del juego
* Cada fila debe contener los números del 1 al 9 sin repetir.
* Cada columna debe contener los números del 1 al 9 sin repetir.
* Cada subcuadrícula de 3x3 debe contener los números del 1 al 9 sin repetir.
* Las casillas iniciales (pistas) no se pueden modificar.

### Niveles de dificultad
* *Fácil:* 40 casillas visibles
* *Medio:* 32 casillas visibles
* *Difícil:* 25 casillas visibles

## Requisitos Funcionales
* *Generación de tablero:* El sistema debe generar un tablero de Sudoku válido y completo en cada partida.
* *Selección de dificultad:* El jugador debe poder elegir el nivel (fácil, medio o difícil) antes de iniciar.
* *Visualización:* El programa debe mostrar el tablero en consola, separando claramente las subcuadrículas de 3x3.
* *Ingreso de jugadas:* El jugador debe poder colocar un número indicando fila, columna y valor.
* *Validación de jugadas:* El sistema debe rechazar los números que repitan valor en la fila, columna o subcuadrícula, e informar el motivo.
* *Protección de pistas:* El programa no debe permitir modificar las casillas iniciales.
* *Borrado de números:* El jugador debe poder borrar un número que colocó.
* *Pistas de ayuda:* El jugador debe poder pedir que se revele una casilla.
* *Resolución automática:* El sistema debe poder resolver el tablero por backtracking.
* *Detección de victoria:* Al completar el tablero correctamente, el programa debe mostrar un mensaje de felicitación y el tiempo de juego.

## Tecnologías y Requisitos del Entorno
* *Lenguaje:* Python 3.14
* *Librerías Estándar (No requieren instalación externa):*
  * `random`: Para generar tableros distintos en cada partida.
  * `copy`: Para duplicar el tablero (solución y tablero de juego).
  * `time`: Para medir el tiempo de la partida.

## Instalación y uso
1. Clonar o descargar el proyecto.
2. Abrir una terminal en la carpeta del proyecto.
3. Ejecutar:
   ```bash
   python sudoku.py
   ```
4. Elegir la dificultad y jugar siguiendo las instrucciones en pantalla.

## Ejemplo de tablero
```
+-------+-------+-------+
| 5 3 . | . 7 . | . . . |
| 6 . . | 1 9 5 | . . . |
| . 9 8 | . . . | . 6 . |
+-------+-------+-------+
| 8 . . | . 6 . | . . 3 |
| 4 . . | 8 . 3 | . . 1 |
| 7 . . | . 2 . | . . 6 |
+-------+-------+-------+
| . 6 . | . . . | 2 8 . |
| . . . | 4 1 9 | . . 5 |
| . . . | . 8 . | . 7 9 |
+-------+-------+-------+
```

## Estructura del proyecto
```
Sudoku/
├── sudoku.py
└── README.md
```
