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
        """Gestiona el inicio de una nueva partida validando el nombre del jugador.

        Genera un nuevo tablero según la dificultad seleccionada, reinicia
        contadores y arranca el cronómetro de la partida.
        """
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

        # Si se borra la celda
        if nuevo_valor == "":
            self.model.matriz_juego[f][c] = 0
            self.view.limpiar_error_celda(f, c)
            return

        if not nuevo_valor.isdigit():
            return

        num = int(nuevo_valor)

        # Validar contra la matriz solución
        if not self.model.es_numero_correcto(f, c, num):
            self.model.errores += 1
            self.view.lbl_errores.config(
                text=f"Errores: {self.model.errores}/5"
            )
            self.view.mostrar_error_celda(f, c)  # Pone el texto/borde en rojo
            self.model.matriz_juego[f][c] = 0

            if self.model.errores >= 5:
                self.partida_activa = False
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
        """Resuelve el tablero automáticamente marcando la partida como no elegible para puntos."""
        if not self.partida_activa:
            return

        self.model.resuelto_auto = True
        self.model.matriz_juego = copy.deepcopy(self.model.matriz_solucion)
        self.view.actualizar_tablero_interfaz(
            self.model.matriz_juego, self.model.matriz_pistas
        )
        self.partida_activa = False
        messagebox.showinfo(
            "Resolución Automática",
            "El sistema ha resuelto el tablero usando Backtracking. Esta partida no sumará puntos.",
        )

    def guardar_partida(self, filepath="partida_guardada.json"):
        """Serializa y guarda el estado actual del juego en un archivo JSON."""
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
                
            messagebox.showinfo("Guardado Exitoso", "La partida se ha guardado correctamente.")
        except OSError as e:
            messagebox.showerror("Error de Guardado", f"No se pudo guardar la partida: {e}")

    def cargar_partida(self, filepath="partida_guardada.json"):
        """Carga el estado del juego desde un archivo JSON y restaura la interfaz."""
        try:
            with open(filepath, "r", encoding="utf-8") as archivo:
                estado_juego = json.load(archivo)
                
            self.model.jugador_actual = estado_juego.get("jugador", "Jugador")
            self.model.dificultad_actual = estado_juego.get("dificultad", "Facil")
            self.model.matriz_juego = estado_juego["matriz_juego"]
            self.model.matriz_solucion = estado_juego["matriz_solucion"]
            self.model.matriz_pistas = estado_juego["matriz_pistas"]
            self.model.errores = estado_juego.get("errores", 0)
            self.model.pistas_usadas = estado_juego.get("pistas_usadas", 0)
            self.segundos_transcurridos = estado_juego.get("segundos_transcurridos", 0)
            self.partida_activa = True
            
            self.view.crear_interfaz_juego(
                self.model.jugador_actual, self.model.dificultad_actual
            )
            self.view.actualizar_tablero_interfaz(
                self.model.matriz_juego, self.model.matriz_pistas
            )
            self.view.lbl_errores.config(text=f"Errores: {self.model.errores}/5")
            self.view.lbl_pistas.config(text=f"Pistas: {self.model.pistas_usadas}")
            
            self.model.tiempo_inicio = time.time() - self.segundos_transcurridos
            self.actualizar_cronometro()
            
            messagebox.showinfo("Carga Exitosa", "La partida se ha restaurado correctamente.")
        except FileNotFoundError:
            messagebox.showwarning("Archivo no encontrado", "No se encontró ninguna partida guardada previa.")
        except (json.JSONDecodeError, KeyError) as e:
            messagebox.showerror("Error de Carga", f"El archivo de guardado está dañado o es inválido: {e}")

    def verificar_estado_final(self):
        """Comprueba si el jugador ha completado con éxito todas las celdas del tablero."""
        if self.model.verificar_victoria():
            self.partida_activa = False
            mins = self.segundos_transcurridos // 60
            segs = self.segundos_transcurridos % 60
            tiempo_str = f"{mins:02d}:{segs:02d}"

            puntaje = self.model.guardar_resultado(self.segundos_transcurridos)

            msg = f"¡Felicidades, {self.model.jugador_actual}! Completaste el Sudoku.\n\n"
            msg += f"Dificultad: {self.model.dificultad_actual}\n"
            msg += f"Tiempo de Juego: {tiempo_str}\n"
            msg += f"Errores cometidos: {self.model.errores}\n"
            msg += f"Pistas de ayuda usadas: {self.model.pistas_usadas}\n"
            if puntaje is not None:
                msg += f"Puntaje obtenido: {puntaje} pts\n"

            messagebox.showinfo("¡Victoria!", msg)
            self.view.crear_interfaz_menu()

    def click_ver_clasificacion(self):
        """Despliega una ventana emergente con el Top 10 de puntuaciones para la dificultad seleccionada."""
        dificultad = self.view.var_dificultad.get()
        top_10 = self.model.obtener_top_10(dificultad)

        ventana_top = tk.Toplevel(self.view)
        ventana_top.title(f"TOP 10 - {dificultad.upper()}")
        ventana_top.geometry("450x320")
        ventana_top.resizable(False, False)

        lbl_t = tk.Label(
            ventana_top,
            text=f"=== TOP 10 - {dificultad.upper()} ===",
            font=("Courier", 12, "bold"),
            pady=10,
        )
        lbl_t.pack()

        txt_area = tk.Text(ventana_top, font=("Courier", 10), width=52, height=12)
        txt_area.pack(pady=5)

        header = f"{'#':<3}{'Jugador':<12}{'Puntaje':<9}{'Tiempo':<9}{'Errores':<9}{'Pistas':<8}\n"
        txt_area.insert(tk.END, header)
        txt_area.insert(tk.END, "-" * 52 + "\n")

        for idx, p in enumerate(top_10, 1):
            m, s = p["tiempo_segundos"] // 60, p["tiempo_segundos"] % 60
            t_str = f"{m:02d}:{s:02d}"
            fila = f"{idx:<3}{p['jugador'][:10]:<12}{p['puntaje']:<9}{t_str:<9}{p['errores']:<9}{p['pistas_usadas']:<8}\n"
            txt_area.insert(tk.END, fila)

        txt_area.config(state="disabled")

    def click_mis_estadisticas(self):
        """Muestra en un cuadro de diálogo el historial estadístico del usuario en el sistema."""
        nombre = self.view.entry_jugador.get().strip()
        if not nombre:
            messagebox.showwarning(
                "Requisito",
                "Ingresa un nombre en el campo para consultar tus estadísticas.",
            )
            return

        stats = self.model.obtener_estadisticas_personales(nombre)
        if not stats:
            messagebox.showinfo(
                "Estadísticas",
                f"No se encontraron registros activos para el jugador: '{nombre}'",
            )
            return

        m, s = stats["mejor_tiempo"] // 60, stats["mejor_tiempo"] % 60
        t_str = f"{m:02d}:{s:02d}" if stats["mejor_tiempo"] > 0 else "N/A"

        msg = f"=== ESTADÍSTICAS DE {nombre.upper()} ===\n\n"
        msg += f"• Partidas jugadas: {stats['jugadas']}\n"
        msg += f"• Partidas ganadas legítimamente: {stats['ganadas']}\n"
        msg += f"• Mejor tiempo registrado: {t_str}\n"
        msg += f"• Promedio de errores: {stats['promedio_errores']:.1f} por partida\n"
        messagebox.showinfo("Estadísticas Personales", msg)