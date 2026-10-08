"""Módulo controlador para el juego Sudoku.

Coordina la interacción entre el modelo de datos (SudokuModel) y la interfaz
gráfica (SudokuView), gestionando el ciclo de vida de las partidas, cronómetro,
validaciones en tiempo real, eventos de usuario y ventanas emergentes.
"""
import copy
import json
import random
import time
import tkinter as tk
from tkinter import messagebox


class SudokuController:
    """Controlador principal de la arquitectura MVC para la aplicación Sudoku."""

    def __init__(self, model, view):
        """Inicializa la instancia del controlador, el modelo, la vista y el estado del juego."""
        self.model = model
        self.view = view
        self.partida_activa = False
        self.segundos_transcurridos = 0

    def iniciar_aplicacion(self):
        """Arranca el bucle de eventos principal de la interfaz de usuario."""
        self.view.mainloop()

    def click_nueva_partida(self):
        """Gestiona el inicio de una nueva partida validando el nombre del jugador."""
        nombre = self.view.entry_jugador.get().strip()
        if not nombre:
            messagebox.showwarning(
                "Requisito", "Por favor, ingresa tu nombre o alias para jugar."
            )
            return

        self.model.generar_nuevo_tablero(self.view.var_dificultad.get())
        self.model.jugador_actual = nombre
        self.partida_activa = True
        self.segundos_transcurridos = 0

        self.view.crear_interfaz_juego(
            self.model.jugador_actual, self.model.dificultad_actual
        )
        self.view.actualizar_tablero_interfaz(
            self.model.matriz_juego, self.model.matriz_pistas
        )
        self.model.tiempo_inicio = time.time()
        self.actualizar_cronometro()

    def actualizar_cronometro(self):
        """Actualiza en segundo plano el tiempo transcurrido en la interfaz cada segundo."""
        if self.partida_activa:
            self.segundos_transcurridos = int(time.time() - self.model.tiempo_inicio)
            mins = self.segundos_transcurridos // 60
            segs = self.segundos_transcurridos % 60
            self.view.lbl_tiempo.config(text=f"Tiempo: {mins:02d}:{segs:02d}")
            self.view.after(1000, self.actualizar_cronometro)

    def modificar_celda(self, f, c, event):
        """Maneja el evento de edición de contenido en una celda del tablero."""
        if not self.partida_activa:
            return

        nuevo_valor = self.view.celdas_ui[(f, c)].get().strip()

        if nuevo_valor == "":
            self.model.matriz_juego[f][c] = 0
            self.view.limpiar_error_celda(f, c)
            return

        if not nuevo_valor.isdigit():
            return

        num = int(nuevo_valor)

        if not self.model.es_numero_correcto(f, c, num):
            self.model.errores += 1
            self.view.lbl_errores.config(
                text=f"Errores: {self.model.errores}/5"
            )
            self.view.mostrar_error_celda(f, c)
            self.model.matriz_juego[f][c] = 0

            if self.model.errores >= 5:
                self.partida_activa = False
                # Registrar derrota automáticamente en JSON con 0 puntos
                self._registrar_fin_juego_json("perdida", 0)

                messagebox.showerror(
                    "Fin del Juego",
                    "Has cometido 5 errores. Has perdido la partida.",
                )
                self.view.crear_interfaz_menu()
        else:
            self.model.matriz_juego[f][c] = num
            self.view.limpiar_error_celda(f, c)
            self.verificar_estado_final()
    
    def click_pedir_pista(self):
        """Otorga una pista revelando una celda vacía aleatoria con su valor correcto."""
        if not self.partida_activa:
            return

        if self.model.pistas_usadas >= 3:
            messagebox.showwarning(
                "Límite de Ayudas",
                "Ya has utilizado tus 3 pistas permitidas para esta partida.",
            )
            return

        celdas_vacias = [
            (f, c)
            for f in range(9)
            for c in range(9)
            if self.model.matriz_juego[f][c] == 0
        ]
        if not celdas_vacias:
            return

        f, c = random.choice(celdas_vacias)
        valor_correcto = self.model.matriz_solucion[f][c]

        self.model.matriz_juego[f][c] = valor_correcto
        self.model.matriz_pistas[f][c] = True
        self.model.pistas_usadas += 1

        self.view.lbl_pistas.config(text=f"Pistas: {self.model.pistas_usadas}")
        self.view.actualizar_tablero_interfaz(
            self.model.matriz_juego, self.model.matriz_pistas
        )
        self.verificar_estado_final()

    def click_auto_resolver(self):
        """Resuelve el tablero automáticamente registrando la partida como auto-resuelta con 0 puntos."""
        if not self.partida_activa:
            return

        self.model.resuelto_auto = True
        self.model.matriz_juego = copy.deepcopy(self.model.matriz_solucion)
        self.view.actualizar_tablero_interfaz(
            self.model.matriz_juego, self.model.matriz_pistas
        )
        self.partida_activa = False

        # Registrar automáticamente en JSON con 0 puntos
        self._registrar_fin_juego_json("auto-resuelta", 0)

        messagebox.showinfo(
            "Resolución Automática",
            "El sistema ha resuelto el tablero. Se ha registrado en tus estadísticas con 0 puntos.",
        )
        self.view.crear_interfaz_menu()

    def guardar_partida(self):
        """Serializa y guarda el estado actual del juego en un archivo JSON específico para el jugador."""
        if not self.partida_activa:
            messagebox.showwarning("Aviso", "No hay ninguna partida activa para guardar.")
            return

        nombre = self.model.jugador_actual.strip()
        nombre_limpio = "".join(c for c in nombre if c.isalnum() or c in ('_', '-')).lower()
        if not nombre_limpio:
            nombre_limpio = "jugador"
        
        filepath = f"partida_{nombre_limpio}.json"

        try:
            estado_juego = {
                "jugador": self.model.jugador_actual,
                "dificultad": self.model.dificultad_actual,
                "matriz_juego": self.model.matriz_juego,
                "matriz_solucion": self.model.matriz_solucion,
                "matriz_pistas": self.model.matriz_pistas,
                "errores": self.model.errores,
                "pistas_usadas": self.model.pistas_usadas,
                "segundos_transcurridos": self.segundos_transcurridos
            }
            with open(filepath, "w", encoding="utf-8") as archivo:
                json.dump(estado_juego, archivo, indent=4)
            messagebox.showinfo("Guardado Exitoso", f"Partida de '{self.model.jugador_actual}' guardada correctamente.")
        except OSError as e:
            messagebox.showerror("Error de Guardado", f"No se pudo guardar la partida: {e}")

    def cargar_partida(self):
        """Carga el estado del juego desde el archivo JSON correspondiente al nombre ingresado."""
        nombre = self.view.entry_jugador.get().strip()
        if not nombre:
            messagebox.showwarning("Requisito", "Ingresa tu nombre para cargar tu partida.")
            return

        nombre_limpio = "".join(c for c in nombre if c.isalnum() or c in ('_', '-')).lower()
        filepath = f"partida_{nombre_limpio}.json"

        try:
            with open(filepath, "r", encoding="utf-8") as archivo:
                estado_juego = json.load(archivo)
                
            self.model.jugador_actual = estado_juego.get("jugador", nombre)
            self.model.dificultad_actual = estado_juego.get("dificultad", "Facil")
            self.model.matriz_juego = estado_juego["matriz_juego"]
            self.model.matriz_solucion = estado_juego["matriz_solucion"]
            self.model.matriz_pistas = estado_juego["matriz_pistas"]
            self.model.errores = estado_juego.get("errores", 0)
            self.model.pistas_usadas = estado_juego.get("pistas_usadas", 0)
            self.segundos_transcurridos = estado_juego.get("segundos_transcurridos", 0)
            self.partida_activa = True
            
            self.view.crear_interfaz_juego(self.model.jugador_actual, self.model.dificultad_actual)
            self.view.actualizar_tablero_interfaz(self.model.matriz_juego, self.model.matriz_pistas)
            self.view.lbl_errores.config(text=f"Errores: {self.model.errores}/5")
            self.view.lbl_pistas.config(text=f"Pistas: {self.model.pistas_usadas}")
            
            self.model.tiempo_inicio = time.time() - self.segundos_transcurridos
            self.actualizar_cronometro()
            
            messagebox.showinfo("Carga Exitosa", f"Partida de '{self.model.jugador_actual}' restaurada.")
        except FileNotFoundError:
            messagebox.showwarning("No encontrada", f"No hay partida guardada para '{nombre}'.")
        except (json.JSONDecodeError, KeyError, OSError) as e:
            messagebox.showerror("Error de Carga", f"El archivo de guardado está dañado o es inválido: {e}")

    def verificar_estado_final(self):
        """Comprueba si el jugador completó con éxito el tablero y guarda estadísticas/puntos."""
        if self.model.verificar_victoria():
            self.partida_activa = False
            mins = self.segundos_transcurridos // 60
            segs = self.segundos_transcurridos % 60
            tiempo_str = f"{mins:02d}:{segs:02d}"

            # Cálculo de puntos (máximo 2000, penalizando tiempo, errores y pistas)
            base_puntos = 2000
            penalizacion_tiempo = self.segundos_transcurridos * 2
            penalizacion_errores = self.model.errores * 150
            penalizacion_pistas = self.model.pistas_usadas * 200
            puntaje = max(base_puntos - penalizacion_tiempo - penalizacion_errores - penalizacion_pistas, 100)

            # Registrar victoria legítima en JSON (suma puntos y va a clasificación)
            self._registrar_fin_juego_json("ganada", puntaje)

            msg = f"¡Felicidades, {self.model.jugador_actual}! Completaste el Sudoku.\n\n"
            msg += f"Dificultad: {self.model.dificultad_actual}\n"
            msg += f"Tiempo: {tiempo_str}\n"
            msg += f"Errores: {self.model.errores}\n"
            msg += f"Pistas: {self.model.pistas_usadas}\n"
            msg += f"Puntaje obtenido: {puntaje} pts (Guardado en clasificación)\n"

            messagebox.showinfo("¡Victoria!", msg)
            self.view.crear_interfaz_menu()

    def _registrar_fin_juego_json(self, resultado, puntos):
        """Guarda automáticamente el resultado de la partida en archivos JSON locales (estadísticas y clasificación)."""
        jugador = self.model.jugador_actual.strip()
        dificultad = self.model.dificultad_actual

        # 1. Gestionar Estadísticas Generales (estadisticas.json)
        try:
            with open("estadisticas.json", "r", encoding="utf-8") as f:
                stats_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            stats_data = {}

        if jugador not in stats_data:
            stats_data[jugador] = {
                "jugadas": 0,
                "ganadas": 0,
                "perdidas": 0,
                "auto_resueltas": 0,
                "mejor_tiempo": 0,
                "total_errores": 0
            }

        stats_data[jugador]["jugadas"] += 1
        stats_data[jugador]["total_errores"] += self.model.errores

        if resultado == "ganada":
            stats_data[jugador]["ganadas"] += 1
            tiempo_actual = self.segundos_transcurridos
            mejor = stats_data[jugador]["mejor_tiempo"]
            if mejor == 0 or tiempo_actual < mejor:
                stats_data[jugador]["mejor_tiempo"] = tiempo_actual
        elif resultado == "perdida":
            stats_data[jugador]["perdidas"] += 1
        elif resultado == "auto-resuelta":
            stats_data[jugador]["auto_resueltas"] += 1

        with open("estadisticas.json", "w", encoding="utf-8") as f:
            json.dump(stats_data, f, indent=4)

        # 2. Gestionar Clasificación / Top 10 (clasificacion.json) - Solo para partidas ganadas
        if resultado == "ganada":
            try:
                with open("clasificacion.json", "r", encoding="utf-8") as f:
                    clas_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                clas_data = {}

            if dificultad not in clas_data:
                clas_data[dificultad] = []

            # Agregar registro a la clasificación de esa dificultad
            registro = {
                "jugador": jugador,
                "puntaje": puntos,
                "tiempo_segundos": self.segundos_transcurridos,
                "errores": self.model.errores,
                "pistas_usadas": self.model.pistas_usadas
            }
            clas_data[dificultad].append(registro)
            # Ordenar por mayor puntaje y menor tiempo
            clas_data[dificultad].sort(key=lambda x: (-x["puntaje"], x["tiempo_segundos"]))
            # Mantener solo los mejores (Top 10)
            clas_data[dificultad] = clas_data[dificultad][:10]

            with open("clasificacion.json", "w", encoding="utf-8") as f:
                json.dump(clas_data, f, indent=4)

    def click_ver_clasificacion(self):
        """Muestra el Top 10 leyendo directamente desde el archivo JSON de clasificación."""
        dificultad = self.view.var_dificultad.get()
        try:
            with open("clasificacion.json", "r", encoding="utf-8") as f:
                clas_data = json.load(f)
            top_10 = clas_data.get(dificultad, [])
        except (FileNotFoundError, json.JSONDecodeError):
            top_10 = []

        ventana_top = tk.Toplevel(self.view)
        ventana_top.title(f"TOP 10 - {dificultad.upper()}")
        ventana_top.geometry("480x320")
        ventana_top.resizable(False, False)

        lbl_t = tk.Label(
            ventana_top,
            text=f"=== TOP 10 - {dificultad.upper()} ===",
            font=("Courier", 12, "bold"),
            pady=10,
        )
        lbl_t.pack()

        txt_area = tk.Text(ventana_top, font=("Courier", 10), width=56, height=12)
        txt_area.pack(pady=5)

        header = f"{'#':<3}{'Jugador':<12}{'Puntaje':<9}{'Tiempo':<9}{'Errores':<9}{'Pistas':<8}\n"
        txt_area.insert(tk.END, header)
        txt_area.insert(tk.END, "-" * 56 + "\n")

        for idx, p in enumerate(top_10, 1):
            m, s = p["tiempo_segundos"] // 60, p["tiempo_segundos"] % 60
            t_str = f"{m:02d}:{s:02d}"
            fila = f"{idx:<3}{p['jugador'][:10]:<12}{p['puntaje']:<9}{t_str:<9}{p['errores']:<9}{p['pistas_usadas']:<8}\n"
            txt_area.insert(tk.END, fila)

        txt_area.config(state="disabled")

    def click_mis_estadisticas(self):
        """Muestra las estadísticas del usuario leyendo directamente desde el archivo JSON."""
        nombre = self.view.entry_jugador.get().strip()
        if not nombre:
            messagebox.showwarning("Requisito", "Ingresa tu nombre para consultar tus estadísticas.")
            return

        try:
            with open("estadisticas.json", "r", encoding="utf-8") as f:
                stats_data = json.load(f)
            stats = stats_data.get(nombre)
        except (FileNotFoundError, json.JSONDecodeError):
            stats = None

        if not stats:
            messagebox.showinfo("Estadísticas", f"No hay registros para el jugador: '{nombre}'")
            return

        m, s = stats["mejor_tiempo"] // 60, stats["mejor_tiempo"] % 60
        t_str = f"{m:02d}:{s:02d}" if stats["mejor_tiempo"] > 0 else "N/A"
        prom_err = stats["total_errores"] / stats["jugadas"] if stats["jugadas"] > 0 else 0

        msg = f"=== ESTADÍSTICAS DE {nombre.upper()} ===\n\n"
        msg += f"• Partidas jugadas: {stats['jugadas']}\n"
        msg += f"• Partidas ganadas: {stats['ganadas']}\n"
        msg += f"• Partidas perdidas (0 pts): {stats['perdidas']}\n"
        msg += f"• Partidas auto-resueltas (0 pts): {stats['auto_resueltas']}\n"
        msg += f"• Mejor tiempo registrado: {t_str}\n"
        msg += f"• Promedio de errores: {prom_err:.1f} por partida\n"
        messagebox.showinfo("Estadísticas Personales", msg)