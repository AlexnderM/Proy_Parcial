"""Módulo para la gestión del modelo de datos y lógica principal del Sudoku.

Contiene el algoritmo de backtracking para resolución y generación de tableros,
así como el control de estado, puntajes y persistencia en formato JSON.
"""

import copy
import json
import os
import random
from datetime import datetime, timezone


class SudokuModel:
    """Representa el modelo de juego de Sudoku y gestiona su estado y reglas."""

    def __init__(self):
        """Inicializa una nueva instancia del modelo con valores por defecto."""
        self.archivo_json = "clasificacion.json"
        self.inicializar_tableros()

    def inicializar_tableros(self):
        """Reinicia las matrices de juego, contadores y variables de estado."""
        self.matriz_solucion = [[0] * 9 for _ in range(9)]
        self.matriz_juego = [[0] * 9 for _ in range(9)]
        self.matriz_pistas = [[False] * 9 for _ in range(9)]
        self.jugador_actual = ""
        self.dificultad_actual = "Fácil"
        self.errores = 0
        self.pistas_usadas = 0
        self.tiempo_inicio = 0
        self.resuelto_auto = False

    def es_valido(self, matriz, fila, col, num):
        """Comprueba si un número se puede colocar en una posición de la matriz.

        Args:
            matriz (list[list[int]]): Matriz de 9x9 con los valores actuales.
            fila (int): Índice de la fila (0 a 8).
            col (int): Índice de la columna (0 a 8).
            num (int): Número a validar (1 a 9).

        Returns:
            bool: True si el movimiento no genera conflictos, False en caso contrario.
        """
        # Validar fila
        if num in matriz[fila]:
            return False
        # Validar columna
        if num in [matriz[f][col] for f in range(9)]:
            return False
        # Validar subcuadrícula 3x3
        ini_f, ini_c = (fila // 3) * 3, (col // 3) * 3
        for f in range(ini_f, ini_f + 3):
            for c in range(ini_c, ini_c + 3):
                if matriz[f][c] == num:
                    return False
        return True

    def resolver_backtracking(self, matriz):
        """Resuelve recursivamente el Sudoku utilizando Backtracking.

        Args:
            matriz (list[list[int]]): Matriz de 9x9 a resolver.

        Returns:
            bool: True si encontró una solución válida, False si la combinación falla.
        """
        for f in range(9):
            for c in range(9):
                if matriz[f][c] == 0:
                    numeros = list(range(1, 10))
                    random.shuffle(numeros)
                    for num in numeros:
                        if self.es_valido(matriz, f, c, num):
                            matriz[f][c] = num
                            if self.resolver_backtracking(matriz):
                                return True
                            matriz[f][c] = 0
                    return False
        return True

    def generar_nuevo_tablero(self, dificultad):
        """Genera un nuevo tablero aleatorio según la dificultad seleccionada.

        Args:
            dificultad (str): Nivel de dificultad ("Fácil", "Medio", "Difícil").
        """
        self.inicializar_tableros()
        self.dificultad_actual = dificultad

        self.resolver_backtracking(self.matriz_solucion)
        self.matriz_juego = copy.deepcopy(self.matriz_solucion)

        visibles = {"Fácil": 40, "Medio": 32, "Difícil": 25}.get(dificultad, 40)
        ocultar = 81 - visibles

        celdas = [(f, c) for f in range(9) for c in range(9)]
        random.shuffle(celdas)

        for i in range(ocultar):
            f, c = celdas[i]
            self.matriz_juego[f][c] = 0

        for f in range(9):
            for c in range(9):
                if self.matriz_juego[f][c] != 0:
                    self.matriz_pistas[f][c] = True

    def es_numero_correcto(self, f: int, c: int, valor: int) -> bool:
        """Verifica si el número ingresado en la posición (f, c) coincide con la matriz solución.

        Args:
            f (int): Índice de la fila.
            c (int): Índice de la columna.
            valor (int): Número a verificar.

        Returns:
            bool: True si coincide con la solución, False en caso contrario.
        """
        return self.matriz_solucion[f][c] == valor
    
    def verificar_victoria(self):
        """Verifica si el tablero está lleno y sin conflictos visuales.

        Returns:
            bool: True si el juego está completo y correcto, False de lo contrario.
        """
        for f in range(9):
            for c in range(9):
                if self.matriz_juego[f][c] == 0:
                    return False
                if self.es_conflicto_visual(f, c, self.matriz_juego[f][c]) is not None:
                    return False
        return True

    def calcular_puntaje(self, segundos):
        """Calcula la puntuación final ponderando tiempo, errores y pistas.

        Args:
            segundos (int): Tiempo de juego transcurrido en segundos.

        Returns:
            int: Puntaje total obtenido (mínimo 0).
        """
        bases = {"Fácil": 500, "Medio": 1000, "Difícil": 1500}
        base = bases.get(self.dificultad_actual, 500)
        puntaje = base - (segundos // 10) - (self.errores * 20) - (self.pistas_usadas * 30)
        return max(0, puntaje)

    def guardar_resultado(self, segundos):
        """Guarda la partida completada en el archivo JSON de historial.

        Args:
            segundos (int): Tiempo total empleado para completar la partida.

        Returns:
            int | None: El puntaje obtenido o None si se resolvió automáticamente.
        """
        if self.resuelto_auto:
            return None

        puntaje = self.calcular_puntaje(segundos)
        nueva_partida = {
            "jugador": self.jugador_actual,
            "dificultad": self.dificultad_actual,
            "puntaje": puntaje,
            "tiempo_segundos": segundos,
            "errores": self.errores,
            "pistas_usadas": self.pistas_usadas,
            "fecha": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "resuelto_auto": False
        }

        datos = {"historial": []}
        if os.path.exists(self.archivo_json):
            try:
                with open(self.archivo_json, "r", encoding="utf-8") as f:
                    datos = json.load(f)
            except Exception(FileNotFoundError, json.JSONDecodeError, KeyError):
                datos = {"historial": []}

        datos["historial"].append(nueva_partida)

        with open(self.archivo_json, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
        return puntaje

    def obtener_top_10(self, dificultad):
        """Obtiene las 10 mejores puntuaciones filtradas por dificultad.

        Args:
            dificultad (str): Nivel de dificultad a consultar.

        Returns:
            list[dict]: Lista ordenada con los diez mejores registros.
        """
        if not os.path.exists(self.archivo_json):
            return []
        try:
            with open(self.archivo_json, "r", encoding="utf-8") as f:
                datos = json.load(f)
            historial = datos.get("historial", [])
            filtrados = [p for p in historial if p["dificultad"] == dificultad and not p.get("resuelto_auto", False)]
            filtrados.sort(key=lambda x: (-x["puntaje"], x["tiempo_segundos"]))
            return filtrados[:10]
        except Exception(FileNotFoundError, json.JSONDecodeError, KeyError):
            return []

    def obtener_estadisticas_personales(self, jugador):
        """Genera un resumen estadístico del desempeño de un jugador.

        Args:
            jugador (str): Nombre del usuario a buscar.

        Returns:
            dict | None: Diccionario con métricas personales o None si no hay partidas.
        """
        if not os.path.exists(self.archivo_json):
            return None
        try:
            with open(self.archivo_json, "r", encoding="utf-8") as f:
                datos = json.load(f)
            historial = [p for p in datos.get("historial", []) if p["jugador"].lower() == jugador.lower()]
            if not historial:
                return None

            jugadas = len(historial)
            ganadas = len([p for p in historial if not p.get("resuelto_auto", False)])
            partidas_validas = [p for p in historial if not p.get("resuelto_auto", False)]

            mejor_tiempo = min([p["tiempo_segundos"] for p in partidas_validas]) if partidas_validas else 0
            promedio_errores = sum([p["errores"] for p in historial]) / jugadas

            return {
                "jugadas": jugadas,
                "ganadas": ganadas,
                "mejor_tiempo": mejor_tiempo,
                "promedio_errores": promedio_errores
            }
        except Exception(FileNotFoundError, json.JSONDecodeError, KeyError, ZeroDivisionError):
            return None

    def es_conflicto_visual(self, fila, col, num):
        """Comprueba si un valor causa un conflicto en fila, columna o bloque 3x3.

        Args:
            fila (int): Fila de la celda.
            col (int): Columna de la celda.
            num (int): Número asignado.

        Returns:
            str | None: Descripción de la regla infringida o None si es válido.
        """
        for c in range(9):
            if c != col and self.matriz_juego[fila][c] == num:
                return "fila"

        for f in range(9):
            if f != fila and self.matriz_juego[f][col] == num:
                return "columna"

        ini_f, ini_c = (fila // 3) * 3, (col // 3) * 3
        for f in range(ini_f, ini_f + 3):
            for c in range(ini_c, ini_c + 3):
                if (f != fila or c != col) and self.matriz_juego[f][c] == num:
                    return "subcuadrícula 3x3"

        return None