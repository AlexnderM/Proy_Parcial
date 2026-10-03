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
        
class SudokuView(tk.Tk):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.title("Sudoku Clásico - Python GUI")
        self.geometry("520x650")
        self.resizable(False, False)
        self.celdas_ui = {}
        self.crear_interfaz_menu()
    def limpiar_ventana(self):
        for widget in self.winfo_children():
            widget.destroy()
    def crear_interfaz_menu(self):
        self.limpiar_ventana()

        frame_menu = tk.Frame(self, padx=20, pady=40, background="#5edfff")
        frame_menu.pack(expand=True, fill="both")
        
        lbl_titulo = tk.Label(frame_menu, text="SUDOKU", font=("Helvetica", 28, "bold"), fg="#1e3d59", bg="#5edfff")
        lbl_titulo.pack(pady=10)
        
        
        lbl_user = tk.Label(frame_menu, text="Nombre del Jugador:", font=("Helvetica", 11))
        lbl_user.pack(pady=5)
        self.entry_jugador = tk.Entry(frame_menu, font=("Helvetica", 12), width=20, justify="center")
        self.entry_jugador.pack(pady=5)
        self.entry_jugador.insert(0, "Tu Nombre")
        
        
        lbl_dif = tk.Label(frame_menu, text="Selecciona la Dificultad:", font=("Helvetica", 11))
        lbl_dif.pack(pady=10)
        
        self.var_dificultad = tk.StringVar(value="Fácil")
        frame_radios = tk.Frame(frame_menu)
        frame_radios.pack()
        for dif in ["Fácil", "Medio", "Difícil"]:
            tk.Radiobutton(frame_radios, text=dif, variable=self.var_dificultad, value=dif, font=("Helvetica", 10)).pack(side="left", padx=10)
            
        
        btn_nueva = tk.Button(frame_menu, text="1. Nueva Partida", font=("Helvetica", 12, "bold"), bg="#5cff3b", fg="#1e2259", width=20, command=self.controlador.click_nueva_partida)
        btn_nueva.pack(pady=10)
        
        btn_clasif = tk.Button(frame_menu, text="2. Ver Clasificación", font=("Helvetica", 11), bg="#1e3d59", fg="white", width=20, command=self.controlador.click_ver_clasificacion)
        btn_clasif.pack(pady=5)
        
        btn_stats = tk.Button(frame_menu, text="3. Mis Estadísticas", font=("Helvetica", 11), bg="#1e3d59", fg="white", width=20, command=self.controlador.click_mis_estadisticas)
        btn_stats.pack(pady=5)
        
        btn_salir = tk.Button(frame_menu, text="4. Salir", font=("Helvetica", 11), bg="#ff6e40", fg="white", width=20, command=self.quit)
        btn_salir.pack(pady=5)
        
        lbl_devs = tk.Label(frame_menu, text="Desarrollado por: Alexander M., Noriel C., Deysi Q.", font=("Helvetica", 8, "italic"), fg="gray")
        lbl_devs.pack(side="bottom")
    def crear_interfaz_juego(self, nombre, dificultad):
        self.limpiar_ventana()

        frame_header = tk.Frame(self, bg="#1e3d59", pady=10)
        frame_header.pack(fill="x")

        lbl_info = tk.Label(frame_header, text=f"Jugador: {nombre}  |  Dificultad: {dificultad}", font=("Helvetica", 11, "bold"), fg="white", bg="#1e3d59")
        lbl_info.pack()
        
        frame_contadores = tk.Frame(self, pady=5, bg="#f3ab10")
        frame_contadores.pack()

        self.lbl_tiempo = tk.Label(frame_contadores, text="Tiempo: 00:00", font=("Helvetica", 11, "bold"), padx=15)
        self.lbl_tiempo.pack(side="left")
        self.lbl_errores = tk.Label(frame_contadores, text="Errores: 0/5", font=("Helvetica", 11, "bold"), fg="#ff0000", padx=15)
        self.lbl_errores.pack(side="left")
        self.lbl_pistas = tk.Label(frame_contadores, text="Pistas: 0/3", font=("Helvetica", 11, "bold"), fg="#17b978", padx=15)
        self.lbl_pistas.pack(side="left")
        frame_tablero_borde = tk.Frame(self, bg="black", bd=2)
        frame_tablero_borde.pack(pady=10)


        self.celdas_ui = {}
        for b_f in range(3):
            for b_c in range(3):
                subcuadrante = tk.Frame(frame_tablero_borde, bg="white", highlightbackground="black", highlightthickness=1, bd=1)
                subcuadrante.grid(row=b_f, column=b_c, padx=1, pady=1)
        
                for f in range(3):
                    for c in range(3):
                        fila_real = b_f * 3 + f
                        col_real = b_c * 3 + c

        frame_tablero_borde = tk.Frame(self, bg="black", bd=2)
        frame_tablero_borde.pack(pady=10)


        self.celdas_ui = {}
        for b_f in range(3):
            for b_c in range(3):
                subcuadrante = tk.Frame(frame_tablero_borde, bg="white", highlightbackground="black", highlightthickness=1, bd=1)
                subcuadrante.grid(row=b_f, column=b_c, padx=1, pady=1)
                
                for f in range(3):
                    for c in range(3):
                        fila_real = b_f * 3 + f
                        col_real = b_c * 3 + c
                        
                        
                        vcmd = (self.register(self.validar_entrada_celda), '%P')
                        entry = tk.Entry(subcuadrante, width=2, font=("Helvetica", 18, "bold"), justify="center", bd=1, validate="key", validatecommand=vcmd)
                        entry.grid(row=f, column=c, padx=2, pady=2, ipady=4)
                        
                       
                        entry.bind("<KeyRelease>", lambda event, r=fila_real, c=col_real: self.controlador.modificar_celda(r, c, event))
                        self.celdas_ui[(fila_real, col_real)] = entry

        frame_acciones = tk.Frame(self, pady=10)
        frame_acciones.pack()

        btn_pista = tk.Button(frame_acciones, text="Pedir Pista", font=("Helvetica", 10, "bold"), bg="#17b978", fg="white", width=12, command=self.controlador.click_pedir_pista)
        btn_pista.grid(row=0, column=0, padx=5)

        btn_resolver = tk.Button(frame_acciones, text="Auto-Resolver", font=("Helvetica", 10, "bold"), bg="#ff6e40", fg="white", width=12, command=self.controlador.click_auto_resolver)
        btn_resolver.grid(row=0, column=1, padx=5)

        btn_menu = tk.Button(frame_acciones, text="Menu Principal", font=("Helvetica", 10), bg="gray", fg="white", width=12, command=self.crear_interfaz_menu)
        btn_menu.grid(row=0, column=2, padx=5)

    def validar_entrada_celda(self, texto):
        if texto == "" or (len(texto) == 1 and texto in "123456789"):
            return True
        return False

    def actualizar_tablero_interfaz(self, matriz_juego, matriz_pistas):
        for (f, c), entry in self.celdas_ui.items():
            valor = matriz_juego[f][c]
            entry.delete(0, tk.END)
            if valor != 0:
                entry.insert(0, str(valor))
            
            if matriz_pistas[f][c]:
                entry.config(state="disabled", disabledbackground="#e0e0e0", disabledforeground="black")
            else:
                entry.config(state="normal", bg="white", fg="#1e3d59")

    def mostrar_error_celda(self, f, c):
        self.celdas_ui[(f, c)].config(bg="#ffcce0", fg="red")

    def limpiar_error_celda(self, f, c):
        self.celdas_ui[(f, c)].config(bg="white", fg="#1e3d59")

