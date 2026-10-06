"""Módulo de la interfaz gráfica de usuario (GUI) para el juego Sudoku.

Define la clase SudokuView utilizando Tkinter, encargada de renderizar
el menú principal, la cuadrícula interactiva de 9x9, contadores de estado,
diálogos de alerta y eventos de usuario.
"""

import tkinter as tk
from tkinter import messagebox


class SudokuView(tk.Tk):
    """Gestor de la interfaz gráfica del juego Sudoku basada en Tkinter."""

    def __init__(self, controlador):
        """Inicializa la ventana principal de la aplicación y sus propiedades.

        Args:
            controlador: Objeto controlador que maneja la lógica de eventos.
        """
        super().__init__()
        self.controlador = controlador
        self.title("Sudoku Clásico - Python GUI")
        self.geometry("520x650")
        self.resizable(False, False)
        self.celdas_ui = {}
        self.crear_interfaz_menu()

    def limpiar_ventana(self):
        """Elimina todos los widgets contenidos en la ventana actual."""
        for widget in self.winfo_children():
            widget.destroy()

    def crear_interfaz_menu(self):
        """Construye y despliega la pantalla del menú principal."""
        self.limpiar_ventana()

        frame_menu = tk.Frame(self, padx=20, pady=40, background="#5edfff")
        frame_menu.pack(expand=True, fill="both")

        lbl_titulo = tk.Label(
            frame_menu,
            text="SUDOKU",
            font=("Helvetica", 28, "bold"),
            fg="#1e3d59",
            bg="#5edfff",
        )
        lbl_titulo.pack(pady=10)

        lbl_user = tk.Label(
            frame_menu, text="Nombre del Jugador:", font=("Helvetica", 11)
        )
        lbl_user.pack(pady=5)
        self.entry_jugador = tk.Entry(
            frame_menu, font=("Helvetica", 12), width=20, justify="center"
        )
        self.entry_jugador.pack(pady=5)
        self.entry_jugador.insert(0, "Tu Nombre")

        lbl_dif = tk.Label(
            frame_menu, text="Selecciona la Dificultad:", font=("Helvetica", 11)
        )
        lbl_dif.pack(pady=10)

        self.var_dificultad = tk.StringVar(value="Fácil")
        frame_radios = tk.Frame(frame_menu)
        frame_radios.pack()
        for dif in ["Fácil", "Medio", "Difícil"]:
            tk.Radiobutton(
                frame_radios,
                text=dif,
                variable=self.var_dificultad,
                value=dif,
                font=("Helvetica", 10),
            ).pack(side="left", padx=10)

        btn_nueva = tk.Button(
            frame_menu,
            text="1. Nueva Partida",
            font=("Helvetica", 12, "bold"),
            bg="#5cff3b",
            fg="#1e2259",
            width=20,
            command=self.controlador.click_nueva_partida,
        )
        btn_nueva.pack(pady=10)

        btn_clasif = tk.Button(
            frame_menu,
            text="2. Ver Clasificación",
            font=("Helvetica", 11),
            bg="#1e3d59",
            fg="white",
            width=20,
            command=self.controlador.click_ver_clasificacion,
        )
        btn_clasif.pack(pady=5)

        btn_stats = tk.Button(
            frame_menu,
            text="3. Mis Estadísticas",
            font=("Helvetica", 11),
            bg="#1e3d59",
            fg="white",
            width=20,
            command=self.controlador.click_mis_estadisticas,
        )
        btn_stats.pack(pady=5)

        btn_salir = tk.Button(
            frame_menu,
            text="4. Salir",
            font=("Helvetica", 11),
            bg="#ff6e40",
            fg="white",
            width=20,
            command=self.quit,
        )
        btn_salir.pack(pady=5)

        lbl_devs = tk.Label(
            frame_menu,
            text="Desarrollado por: Alexander M., Noriel C., Deysi Q.",
            font=("Helvetica", 8, "italic"),
            fg="gray",
        )
        lbl_devs.pack(side="bottom")

    def crear_interfaz_juego(self, nombre, dificultad):
        """Construye y visualiza el tablero interactivo de juego y sus controles.

        Args:
            nombre (str): Nombre del jugador activo.
            dificultad (str): Nivel de dificultad seleccionado.
        """
        self.limpiar_ventana()

        frame_header = tk.Frame(self, bg="#1e3d59", pady=10)
        frame_header.pack(fill="x")

        lbl_info = tk.Label(
            frame_header,
            text=f"Jugador: {nombre}  |  Dificultad: {dificultad}",
            font=("Helvetica", 11, "bold"),
            fg="white",
            bg="#1e3d59",
        )
        lbl_info.pack()

        frame_contadores = tk.Frame(self, pady=5, bg="#f3ab10")
        frame_contadores.pack()

        self.lbl_tiempo = tk.Label(
            frame_contadores, text="Tiempo: 00:00", font=("Helvetica", 11, "bold"), padx=15
        )
        self.lbl_tiempo.pack(side="left")

        self.lbl_errores = tk.Label(
            frame_contadores,
            text="Errores: 0/5",
            font=("Helvetica", 11, "bold"),
            fg="#ff0000",
            padx=15,
        )
        self.lbl_errores.pack(side="left")

        self.lbl_pistas = tk.Label(
            frame_contadores,
            text="Pistas: 0/3",
            font=("Helvetica", 11, "bold"),
            fg="#17b978",
            padx=15,
        )
        self.lbl_pistas.pack(side="left")

        frame_tablero_borde = tk.Frame(self, bg="black", bd=2)
        frame_tablero_borde.pack(pady=10)

        self.celdas_ui = {}
        for b_f in range(3):
            for b_c in range(3):
                subcuadrante = tk.Frame(
                    frame_tablero_borde,
                    bg="white",
                    highlightbackground="black",
                    highlightthickness=1,
                    bd=1,
                )
                subcuadrante.grid(row=b_f, column=b_c, padx=1, pady=1)

                for f in range(3):
                    for c in range(3):
                        fila_real = b_f * 3 + f
                        col_real = b_c * 3 + c

                        vcmd = (self.register(self.validar_entrada_celda), "%P")
                        entry = tk.Entry(
                            subcuadrante,
                            width=2,
                            font=("Helvetica", 18, "bold"),
                            justify="center",
                            bd=1,
                            validate="key",
                            validatecommand=vcmd,
                        )
                        entry.grid(row=f, column=c, padx=2, pady=2, ipady=4)

                        entry.bind(
                            "<KeyRelease>",
                            lambda event, r=fila_real, c=col_real: self.controlador.modificar_celda(
                                r, c, event
                            ),
                        )
                        self.celdas_ui[(fila_real, col_real)] = entry

        frame_acciones = tk.Frame(self, pady=10)
        frame_acciones.pack()

        btn_pista = tk.Button(
            frame_acciones,
            text="Pedir Pista",
            font=("Helvetica", 10, "bold"),
            bg="#17b978",
            fg="white",
            width=12,
            command=self.controlador.click_pedir_pista,
        )
        btn_pista.grid(row=0, column=0, padx=5)

        btn_resolver = tk.Button(
            frame_acciones,
            text="Auto-Resolver",
            font=("Helvetica", 10, "bold"),
            bg="#ff6e40",
            fg="white",
            width=12,
            command=self.controlador.click_auto_resolver,
        )
        btn_resolver.grid(row=0, column=1, padx=5)

        btn_menu = tk.Button(
            frame_acciones,
            text="Menu Principal",
            font=("Helvetica", 10),
            bg="gray",
            fg="white",
            width=12,
            command=self.crear_interfaz_menu,
        )
        btn_menu.grid(row=0, column=2, padx=5)

    def validar_entrada_celda(self, texto):
        """Valida que la entrada del usuario en las celdas sea vacía o un dígito del 1 al 9.

        Args:
            texto (str): Cadena enviada por el evento de validación.

        Returns:
            bool: True si el texto es válido para la entrada, False de lo contrario.
        """
        if texto == "" or (len(texto) == 1 and texto in "123456789"):
            return True
        return False

    def actualizar_tablero_interfaz(self, matriz_juego, matriz_pistas):
        """Sincroniza los valores numéricos y el estado bloqueado de las celdas en pantalla.

        Args:
            matriz_juego (list[list[int]]): Matriz con el estado del tablero actual.
            matriz_pistas (list[list[bool]]): Matriz booleana con celdas iniciales/pistas.
        """
        for (f, c), entry in self.celdas_ui.items():
            valor = matriz_juego[f][c]
            entry.delete(0, tk.END)
            if valor != 0:
                entry.insert(0, str(valor))

            if matriz_pistas[f][c]:
                entry.config(
                    state="disabled",
                    disabledbackground="#e0e0e0",
                    disabledforeground="black",
                )
            else:
                entry.config(state="normal", bg="white", fg="#1e3d59")

    def mostrar_error_celda(self, f, c):
        """Resalta en color rojo una celda que contiene un número en conflicto.

        Args:
            f (int): Fila de la celda.
            c (int): Columna de la celda.
        """
        self.celdas_ui[(f, c)].config(bg="#ffcce0", fg="red")

    def limpiar_error_celda(self, f, c):
        """Restablece el estilo visual normal de una celda previamente marcada con error.

        Args:
            f (int): Fila de la celda.
            c (int): Columna de la celda.
        """
        self.celdas_ui[(f, c)].config(bg="white", fg="#1e3d59")