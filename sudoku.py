import tkinter as tk
from tkinter import messagebox, ttk
import random
import copy
import time
import json
import os
from datetime import datetime

class SudokuModel:
    def __init__(self):
        self.archivo_json = "clasificacion.json"
        self.inicializar_tableros()
        
    def inicializar_tableros(self):
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
        if num in matriz[fila]:
            return False
        if num in [matriz[f][col] for f in range(9)]:
            return False
        ini_f, ini_c = (fila // 3) * 3, (col // 3) * 3
        for f in range(ini_f, ini_f + 3):
            for c in range(ini_c, ini_c + 3):
                if matriz[f][c] == num:
                    return False
        return True

    def resolver_backtracking(self, matriz):
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

    def verificar_victoria(self):
        for f in range(9):
            for c in range(9):
                if self.matriz_juego[f][c] == 0:
                    return False
                if self.es_conflicto_visual(f, c, self.matriz_juego[f][c]) is not None:
                    return False
        return True

    def calcular_puntaje(self, segundos):
        bases = {"Fácil": 500, "Medio": 1000, "Difícil": 1500}
        base = bases.get(self.dificultad_actual, 500)
        puntaje = base - (segundos // 10) - (self.errores * 20) - (self.pistas_usadas * 30)
        return max(0, puntaje)

    def guardar_resultado(self, segundos):
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
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "resuelto_auto": False
        }
        
        datos = {"historial": []}
        if os.path.exists(self.archivo_json):
            try:
                with open(self.archivo_json, "r", encoding="utf-8") as f:
                    datos = json.load(f)
            except:
                pass
                
        datos["historial"].append(nueva_partida)
        
        with open(self.archivo_json, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
        return puntaje

    def obtener_top_10(self, dificultad):
        if not os.path.exists(self.archivo_json):
            return []
        try:
            with open(self.archivo_json, "r", encoding="utf-8") as f:
                datos = json.load(f)
            historial = datos.get("historial", [])
            filtrados = [p for p in historial if p["dificultad"] == dificultad and not p.get("resuelto_auto", False)]
            filtrados.sort(key=lambda x: (-x["puntaje"], x["tiempo_segundos"]))
            return filtrados[:10]
        except:
            return []

    def obtener_estadisticas_personales(self, jugador):
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
        except:
            return None

    def es_conflicto_visual(self, fila, col, num):
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
