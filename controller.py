import time
import random
import copy
import tkinter as tk
from tkinter import messagebox
from model import SudokuModel
from view import SudokuView

class SudokuController:
    def __init__(self):
        self.model = SudokuModel()
        self.view = SudokuView(self)
        self.partida_activa = False
        self.segundos_transcurridos = 0

    def iniciar_aplicacion(self):
        self.view.mainloop()

    def click_nueva_partida(self):
        nombre = self.view.entry_jugador.get().strip()
        if not nombre:
            messagebox.showwarning("Requisito", "Por favor, ingresa tu nombre o alias para jugar.")
            return
        self.model.generar_nuevo_tablero(self.view.var_dificultad.get())
        self.model.jugador_actual = nombre
        self.partida_activa = True
        self.segundos_transcurridos = 0
        self.view.crear_interfaz_juego(self.model.jugador_actual, self.model.dificultad_actual)
        self.view.actualizar_tablero_interfaz(self.model.matriz_juego, self.model.matriz_pistas)
        self.model.tiempo_inicio = time.time()
        self.actualizar_cronometro()

    def actualizar_cronometro(self):
        if self.partida_activa:
            self.segundos_transcurridos = int(time.time() - self.model.tiempo_inicio)
            mins = self.segundos_transcurridos // 60
            segs = self.segundos_transcurridos % 60
            self.view.lbl_tiempo.config(text=f"Tiempo: {mins:02d}:{segs:02d}")
            self.view.after(1000, self.actualizar_cronometro)

    def modificar_celda(self, f, c, event):
        if not self.partida_activa:
            return

        nuevo_valor = self.view.celdas_ui[(f, c)].get().strip()

        if nuevo_valor == "":
            self.model.matriz_juego[f][c] = 0
            self.view.limpiar_error_celda(f, c)
            return

        num = int(nuevo_valor)

        motivo_conflicto = self.model.es_conflicto_visual(f, c, num)

        if motivo_conflicto:
            self.model.errores += 1
            self.view.lbl_errores.config(
                text=f"Errores: {self.model.errores}/5"
            )
            self.view.mostrar_error_celda(f, c)
            self.model.matriz_juego[f][c] = 0

            if self.model.errores >= 5:
                self.partida_activa = False
                messagebox.showerror(
                    "Fin del Juego",
                    "Has cometido 5 errores. Has perdido la partida.",
                )
                self.view.crear_interfaz_menu()
                return

            messagebox.showerror(
                "Movimiento Inválido",
                f"El número {num} ya existe en la {motivo_conflicto}.",
            )
        else:
            self.model.matriz_juego[f][c] = num
            self.view.limpiar_error_celda(f, c)

            self.verificar_estado_final()


    def click_pedir_pista(self):
        if not self.partida_activa: 
            return
          
        if self.model.pistas_usadas >= 3:
            messagebox.showwarning("Límite de Ayudas", "Ya has utilizado tus 3 pistas permitidas para esta partida.")
            return
        
        celdas_vacias = [(f, c) for f in range(9) for c in range(9) if self.model.matriz_juego[f][c] == 0]
        if not celdas_vacias: 
            return
            
        f, c = random.choice(celdas_vacias)
        valor_correcto = self.model.matriz_solucion[f][c]
        
        self.model.matriz_juego[f][c] = valor_correcto
        self.model.matriz_pistas[f][c] = True
        self.model.pistas_usadas += 1
        
        self.view.lbl_pistas.config(text=f"Pistas: {self.model.pistas_usadas}")
        self.view.actualizar_tablero_interfaz(self.model.matriz_juego, self.model.matriz_pistas)
        self.verificar_estado_final()


    def click_auto_resolver(self):
        if not self.partida_activa: 
            return
        self.model.resuelto_auto = True
        self.model.matriz_juego = copy.deepcopy(self.model.matriz_solucion)
        self.view.actualizar_tablero_interfaz(self.model.matriz_juego, self.model.matriz_pistas)
        self.partida_activa = False
        messagebox.showinfo("Resolución Automática", "El sistema ha resuelto el tablero usando Backtracking. Esta partida no sumará puntos.")

    def verificar_estado_final(self):
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
        dificultad = self.view.var_dificultad.get()
        top_10 = self.model.obtener_top_10(dificultad)
        ventana_top = tk.Toplevel(self.view)
        ventana_top.title(f"TOP 10 - {dificultad.upper()}")
        ventana_top.geometry("450x320")
        ventana_top.resizable(False, False)
            
        lbl_t = tk.Label(ventana_top, text=f"=== TOP 10 - {dificultad.upper()} ===", font=("Courier", 12, "bold"), pady=10)
        lbl_t.pack()
            
        txt_area = tk.Text(ventana_top, font=("Courier", 10), width=52, height=12)
        txt_area.pack(pady=5)
            
        header = f"{'#':<3}{'Jugador':<12}{'Puntaje':<9}{'Tiempo':<9}{'Errores':<9}{'Pistas':<8}\n"
        txt_area.insert(tk.END, header)
        txt_area.insert(tk.END, "-"*52 + "\n")
            
        for idx, p in enumerate(top_10, 1):
            m, s = p['tiempo_segundos'] // 60, p['tiempo_segundos'] % 60
            t_str = f"{m:02d}:{s:02d}"
            fila = f"{idx:<3}{p['jugador'][:10]:<12}{p['puntaje']:<9}{t_str:<9}{p['errores']:<9}{p['pistas_usadas']:<8}\n"
            txt_area.insert(tk.END, fila)
                
        txt_area.config(state="disabled")

    def click_mis_estadisticas(self):
        nombre = self.view.entry_jugador.get().strip()
        if not nombre:
            messagebox.showwarning("Requisito", "Ingresa un nombre en el campo para consultar tus estadísticas.")
            return
            
        stats = self.model.obtener_estadisticas_personales(nombre)
        if not stats:
            messagebox.showinfo("Estadísticas", f"No se encontraron registros activos para el jugador: '{nombre}'")
            return
            
        m, s = stats['mejor_tiempo'] // 60, stats['mejor_tiempo'] % 60
        t_str = f"{m:02d}:{s:02d}" if stats['mejor_tiempo'] > 0 else "N/A"
        
        msg = f"=== ESTADÍSTICAS DE {nombre.upper()} ===\n\n"
        msg += f"• Partidas jugadas: {stats['jugadas']}\n"
        msg += f"• Partidas ganadas legítimamente: {stats['ganadas']}\n"
        msg += f"• Mejor tiempo registrado: {t_str}\n"
        msg += f"• Promedio de errores: {stats['promedio_errores']:.1f} por partida\n"
        messagebox.showinfo("Estadísticas Personales", msg)