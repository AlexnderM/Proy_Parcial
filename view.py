"""Módulo de la interfaz gráfica de usuario (GUI) para el juego Sudoku.

Define la clase SudokuView utilizando Tkinter, encargada de renderizar
el menú principal, la cuadrícula interactiva de 9x9, contadores de estado,
diálogos de alerta y eventos de usuario.
"""

import tkinter as tk

FUENTE = "Helvetica"
COLOR_FONDO = "#EEF2F7"
COLOR_TARJETA = "#FFFFFF"
COLOR_PRIMARIO = "#1E3A5F"
COLOR_ACENTO = "#3B82F6"
COLOR_EXITO = "#16A34A"
COLOR_PELIGRO = "#DC2626"
COLOR_NEUTRO = "#64748B"
COLOR_TEXTO = "#1E293B"
COLOR_BORDE = "#CBD5E1"
COLOR_CELDA_FIJA = "#E2E8F0"
COLOR_ERROR_FONDO = "#FEE2E2"


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
        self.configure(bg=COLOR_FONDO)
        self.celdas_ui = {}
        self.crear_interfaz_menu()

    def limpiar_ventana(self):
        """Elimina todos los widgets contenidos en la ventana actual."""
        for widget in self.winfo_children():
            widget.destroy()

    def volver_menu(self):
        """Detiene la partida en curso y regresa al menú principal."""
        self.controlador.partida_activa = False
        self.crear_interfaz_menu()

    def _limpiar_nombre_inicial(self, event):
        """Borra el texto de ejemplo del campo de nombre al enfocarlo.

        Args:
            event: Evento de foco de Tkinter (<FocusIn>).
        """
        if self.entry_jugador.get() == "Tu Nombre":
            self.entry_jugador.delete(0, tk.END)

    def _crear_boton(self, padre, texto, color, comando, negrita=True):
        """Crea un botón plano con el estilo visual de la aplicación.

        Args:
            padre: Widget contenedor del botón.
            texto (str): Texto que muestra el botón.
            color (str): Color de fondo del botón en formato hexadecimal.
            comando: Función que se ejecuta al presionar el botón.
            negrita (bool): Indica si el texto se muestra en negrita.

        Returns:
            tk.Button: El botón creado.
        """
        return tk.Button(
            padre,
            text=texto,
            font=(FUENTE, 11, "bold" if negrita else "normal"),
            bg=color,
            fg="white",
            activebackground=COLOR_PRIMARIO,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=6,
            width=22,
            command=comando,
        )

    def crear_interfaz_menu(self):
        """Construye y despliega la pantalla del menú principal."""
        self.limpiar_ventana()

        frame_menu = tk.Frame(self, padx=30, pady=30, bg=COLOR_FONDO)
        frame_menu.pack(expand=True, fill="both")

        lbl_titulo = tk.Label(
            frame_menu,
            text="SUDOKU",
            font=(FUENTE, 36, "bold"),
            fg=COLOR_PRIMARIO,
            bg=COLOR_FONDO,
        )
        lbl_titulo.pack(pady=(20, 0))

        lbl_subtitulo = tk.Label(
            frame_menu,
            text="Clásico · Python GUI",
            font=(FUENTE, 11),
            fg=COLOR_NEUTRO,
            bg=COLOR_FONDO,
        )
        lbl_subtitulo.pack(pady=(0, 25))

        tarjeta = tk.Frame(
            frame_menu,
            bg=COLOR_TARJETA,
            padx=30,
            pady=25,
            highlightbackground=COLOR_BORDE,
            highlightthickness=1,
        )
        tarjeta.pack(fill="x", padx=20)

        lbl_user = tk.Label(
            tarjeta,
            text="Nombre del jugador",
            font=(FUENTE, 10, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_TARJETA,
        )
        lbl_user.pack(anchor="w")

        self.entry_jugador = tk.Entry(
            tarjeta,
            font=(FUENTE, 12),
            justify="center",
            relief="flat",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            highlightthickness=1,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_ACENTO,
        )
        self.entry_jugador.pack(fill="x", pady=(4, 15), ipady=6)
        self.entry_jugador.insert(0, "Tu Nombre")
        self.entry_jugador.bind("<FocusIn>", self._limpiar_nombre_inicial)

        lbl_dif = tk.Label(
            tarjeta,
            text="Dificultad",
            font=(FUENTE, 10, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_TARJETA,
        )
        lbl_dif.pack(anchor="w")

        self.var_dificultad = tk.StringVar(value="Fácil")
        frame_radios = tk.Frame(tarjeta, bg=COLOR_TARJETA)
        frame_radios.pack(fill="x", pady=(4, 20))
        for dif in ["Fácil", "Medio", "Difícil"]:
            tk.Radiobutton(
                frame_radios,
                text=dif,
                variable=self.var_dificultad,
                value=dif,
                indicatoron=False,
                font=(FUENTE, 10, "bold"),
                bg=COLOR_FONDO,
                fg=COLOR_TEXTO,
                selectcolor=COLOR_ACENTO,
                activebackground=COLOR_BORDE,
                relief="flat",
                bd=0,
                cursor="hand2",
                pady=6,
            ).pack(side="left", expand=True, fill="x", padx=2)

        self._crear_boton(
            tarjeta,
            "Nueva Partida",
            COLOR_EXITO,
            self.controlador.click_nueva_partida,
        ).pack(fill="x", pady=4)

        self._crear_boton(
            tarjeta,
            "Ver Clasificación",
            COLOR_PRIMARIO,
            self.controlador.click_ver_clasificacion,
            negrita=False,
        ).pack(fill="x", pady=4)

        self._crear_boton(
            tarjeta,
            "Mis Estadísticas",
            COLOR_PRIMARIO,
            self.controlador.click_mis_estadisticas,
            negrita=False,
        ).pack(fill="x", pady=4)

        self._crear_boton(
            tarjeta,
            "Salir",
            COLOR_PELIGRO,
            self.quit,
            negrita=False,
        ).pack(fill="x", pady=4)

        lbl_devs = tk.Label(
            frame_menu,
            text="Desarrollado por: Alexander M., Noriel C., Deysi Q.",
            font=(FUENTE, 8, "italic"),
            fg=COLOR_NEUTRO,
            bg=COLOR_FONDO,
        )
        lbl_devs.pack(side="bottom")

    def crear_interfaz_juego(self, nombre, dificultad):
        """Construye y visualiza el tablero interactivo de juego y sus controles.

        Args:
            nombre (str): Nombre del jugador activo.
            dificultad (str): Nivel de dificultad seleccionado.
        """
        self.limpiar_ventana()

        frame_header = tk.Frame(self, bg=COLOR_PRIMARIO, pady=12)
        frame_header.pack(fill="x")

        lbl_info = tk.Label(
            frame_header,
            text=f"Jugador: {nombre}  |  Dificultad: {dificultad}",
            font=(FUENTE, 11, "bold"),
            fg="white",
            bg=COLOR_PRIMARIO,
        )
        lbl_info.pack()

        frame_contadores = tk.Frame(
            self,
            bg=COLOR_TARJETA,
            pady=8,
            highlightbackground=COLOR_BORDE,
            highlightthickness=1,
        )
        frame_contadores.pack(pady=(15, 5))

        self.lbl_tiempo = tk.Label(
            frame_contadores,
            text="Tiempo: 00:00",
            font=(FUENTE, 11, "bold"),
            fg=COLOR_PRIMARIO,
            bg=COLOR_TARJETA,
            padx=15,
        )
        self.lbl_tiempo.pack(side="left")

        self.lbl_errores = tk.Label(
            frame_contadores,
            text="Errores: 0/5",
            font=(FUENTE, 11, "bold"),
            fg=COLOR_PELIGRO,
            bg=COLOR_TARJETA,
            padx=15,
        )
        self.lbl_errores.pack(side="left")

        self.lbl_pistas = tk.Label(
            frame_contadores,
            text="Pistas: 0/3",
            font=(FUENTE, 11, "bold"),
            fg=COLOR_EXITO,
            bg=COLOR_TARJETA,
            padx=15,
        )
        self.lbl_pistas.pack(side="left")

        frame_tablero_borde = tk.Frame(self, bg=COLOR_PRIMARIO, bd=0, padx=3, pady=3)
        frame_tablero_borde.pack(pady=10)

        vcmd = (self.register(self.validar_entrada_celda), "%P")

        self.celdas_ui = {}
        for b_f in range(3):
            for b_c in range(3):
                subcuadrante = tk.Frame(frame_tablero_borde, bg=COLOR_PRIMARIO)
                subcuadrante.grid(row=b_f, column=b_c, padx=1, pady=1)

                for f in range(3):
                    for c in range(3):
                        fila_real = b_f * 3 + f
                        col_real = b_c * 3 + c

                        entry = tk.Entry(
                            subcuadrante,
                            width=2,
                            font=(FUENTE, 18, "bold"),
                            justify="center",
                            relief="flat",
                            bd=0,
                            bg="white",
                            fg=COLOR_ACENTO,
                            highlightthickness=1,
                            highlightbackground=COLOR_BORDE,
                            highlightcolor=COLOR_ACENTO,
                            validate="key",
                            validatecommand=vcmd,
                        )
                        entry.grid(row=f, column=c, ipady=6)

                        entry.bind(
                            "<KeyRelease>",
                            lambda event, fila=fila_real, col=col_real: (
                                self._al_soltar_tecla(fila, col, event)
                            ),
                        )
                        self.celdas_ui[(fila_real, col_real)] = entry

        frame_acciones = tk.Frame(self, bg=COLOR_FONDO, pady=10)
        frame_acciones.pack()

        botones = [
            ("Pedir Pista", COLOR_EXITO, self.controlador.click_pedir_pista, True),
            (
                "Auto-Resolver",
                COLOR_PELIGRO,
                self.controlador.click_auto_resolver,
                True,
            ),
            ("Menú Principal", COLOR_NEUTRO, self.volver_menu, False),
        ]
        for columna, (texto, color, comando, negrita) in enumerate(botones):
            btn = self._crear_boton(frame_acciones, texto, color, comando, negrita)
            btn.config(width=13, font=(FUENTE, 10, "bold" if negrita else "normal"))
            btn.grid(row=0, column=columna, padx=5)

    def _al_soltar_tecla(self, fila, col, event):
        """Reenvía al controlador solo las teclas que modifican una celda.

        Ignora flechas, Tab, Shift y otras teclas que no cambian el contenido,
        para que no se cuenten como movimientos del jugador.

        Args:
            fila (int): Fila de la celda donde se soltó la tecla.
            col (int): Columna de la celda donde se soltó la tecla.
            event: Evento de teclado de Tkinter (<KeyRelease>).
        """
        if event.keysym in ("BackSpace", "Delete") or event.char.isdigit():
            self.controlador.modificar_celda(fila, col, event)

    def validar_entrada_celda(self, texto):
        """Valida que la entrada del usuario en las celdas sea vacía o un dígito del 1 al 9.

        Args:
            texto (str): Cadena enviada por el evento de validación.

        Returns:
            bool: True si el texto es válido para la entrada, False de lo contrario.
        """
        return texto == "" or (len(texto) == 1 and texto in "123456789")

    def actualizar_tablero_interfaz(self, matriz_juego, matriz_pistas):
        """Sincroniza los valores numéricos y el estado bloqueado de las celdas en pantalla.

        Args:
            matriz_juego (list[list[int]]): Matriz con el estado del tablero actual.
            matriz_pistas (list[list[bool]]): Matriz booleana con celdas iniciales/pistas.
        """
        for (f, c), entry in self.celdas_ui.items():
            entry.config(state="normal")
            valor = matriz_juego[f][c]
            entry.delete(0, tk.END)
            if valor != 0:
                entry.insert(0, str(valor))

            if matriz_pistas[f][c]:
                entry.config(
                    state="disabled",
                    disabledbackground=COLOR_CELDA_FIJA,
                    disabledforeground=COLOR_TEXTO,
                )
            else:
                entry.config(bg="white", fg=COLOR_ACENTO)

    def mostrar_error_celda(self, f, c):
        """Resalta en color rojo una celda que contiene un número en conflicto.

        Args:
            f (int): Fila de la celda.
            c (int): Columna de la celda.
        """
        self.celdas_ui[(f, c)].config(bg=COLOR_ERROR_FONDO, fg=COLOR_PELIGRO)

    def limpiar_error_celda(self, f, c):
        """Restablece el estilo visual normal de una celda previamente marcada con error.

        Args:
            f (int): Fila de la celda.
            c (int): Columna de la celda.
        """
        self.celdas_ui[(f, c)].config(bg="white", fg=COLOR_ACENTO)