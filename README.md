# Sudoku

Juego de Sudoku clásico en Python. Permite generar tableros con distintos niveles de dificultad, jugar validando cada jugada, resolver el tablero automáticamente y competir en una tabla de clasificación por jugador y dificultad.

## Desarrolladores del proyecto
- Alexander Madrid
- Noriel Cortes
- Deysi Quintero

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
* *Registro de jugadores:* Al iniciar, el jugador debe ingresar su nombre o alias para asociar sus partidas.
* *Guardado de resultados:* Al ganar, el sistema debe guardar nombre, dificultad, tiempo, errores, pistas usadas y fecha.
* *Tabla de clasificación:* El programa debe mostrar el Top 10 por dificultad, ordenado del mejor al peor resultado.
* *Estadísticas personales:* El jugador debe poder consultar sus partidas jugadas, ganadas, mejor tiempo y promedio.
* *Persistencia:* Los resultados deben conservarse entre sesiones en un archivo local.

## Sistema de Clasificación
Cada partida ganada suma un puntaje. La tabla se ordena por puntaje (de mayor a menor) y, en caso de empate, por menor tiempo.

### Cálculo del puntaje
```
puntaje = base_dificultad - (segundos // 10) - (errores * 20) - (pistas * 30)
```
* *Base por dificultad:* Fácil 500, Medio 1000, Difícil 1500.
* *Penalizaciones:* tiempo empleado, errores cometidos y pistas usadas.
* *Mínimo:* el puntaje nunca baja de 0.
* *Resolución automática:* si el jugador usa "resolver", la partida no entra en la clasificación.

### Ejemplo de tabla
```
=== TOP 10 - DIFÍCIL ===
 #  Jugador     Puntaje   Tiempo   Errores  Pistas  Fecha
 1  Noriel        1180    08:45       1       0     2026-09-28
 2  Deysi         1090    10:12       2       1     2026-09-27
 3  Alexander      950    12:30       3       1     2026-09-26
```

### Menú principal
```
1. Nueva partida
2. Ver clasificación
3. Mis estadísticas
4. Salir
```

## Tecnologías y Requisitos del Entorno
* *Lenguaje:* Python 3.14
* *Librerías Estándar (No requieren instalación externa):*
  * `random`: Para generar tableros distintos en cada partida.
  * `copy`: Para duplicar el tablero (solución y tablero de juego).
  * `time`: Para medir el tiempo de la partida.
  * `json`: Para guardar y leer la clasificación en `clasificacion.json`.
  * `datetime`: Para registrar la fecha de cada partida.
  * `TKinter`: Desarrollo de la interfaz gráfica.

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
├── clasificacion.json   (se crea automáticamente)
└── README.md
```
