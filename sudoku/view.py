"""Módulo de la interfaz gráfica de usuario (GUI) para el juego Sudoku.

Define la clase SudokuView utilizando Tkinter, encargada de renderizar
el menú principal, la cuadrícula interactiva de 9x9, contadores de estado,
diálogos de alerta y eventos de usuario.
"""

import math
import random
import time
import tkinter as tk
from tkinter import font as tkfont

FUENTE = "Helvetica"

PALABRAS_VICTORIA = (
    "¡Felicidades!",
    "¡Fantástico!",
    "¡Excelente!",
    "¡Increíble!",
    "¡Genial!",
    "¡Espectacular!",
    "¡Bien hecho!",
    "¡Magnífico!",
    "¡Impresionante!",
    "¡Brillante!",
)
COLORES_CONFETI = ("#F87171", "#FBBF24", "#34D399", "#60A5FA", "#A78BFA", "#F472B6")
DURACION_CELEBRACION_MS = 5500

PALETAS = {
    "claro": {
        "fondo": "#EEF2F7",
        "tarjeta": "#FFFFFF",
        "entrada": "#EEF2F7",
        "titulo": "#1E3A5F",
        "encabezado": "#1E3A5F",
        "marco_tablero": "#1E3A5F",
        "secundario": "#1E3A5F",
        "boton_neutro": "#64748B",
        "texto": "#1E293B",
        "subtexto": "#64748B",
        "borde": "#CBD5E1",
        "acento": "#3B82F6",
        "seleccion": "#3B82F6",
        "digito": "#3B82F6",
        "exito": "#16A34A",
        "peligro": "#DC2626",
        "celda": "#FFFFFF",
        "celda_fija": "#E2E8F0",
        "error_fondo": "#FEE2E2",
        "parpadeo": "#FCA5A5",
        "activa": "#BFDBFE",
        "relacion": "#EAF1FB",
        "fija_relacion": "#D5E2F5",
        "mismo_numero": "#FDE68A",
        "ola": "#93C5FD",
        "pista": "#4ADE80",
        "destello": "#86EFAC",
    },
    "oscuro": {
        "fondo": "#0F172A",
        "tarjeta": "#1E293B",
        "entrada": "#0F172A",
        "titulo": "#E2E8F0",
        "encabezado": "#172554",
        "marco_tablero": "#94A3B8",
        "secundario": "#334155",
        "boton_neutro": "#475569",
        "texto": "#E2E8F0",
        "subtexto": "#94A3B8",
        "borde": "#334155",
        "acento": "#60A5FA",
        "seleccion": "#2563EB",
        "digito": "#93C5FD",
        "exito": "#16A34A",
        "peligro": "#EF4444",
        "celda": "#111C33",
        "celda_fija": "#263449",
        "error_fondo": "#7F1D1D",
        "parpadeo": "#B91C1C",
        "activa": "#1E3A8A",
        "relacion": "#17233F",
        "fija_relacion": "#2B3A55",
        "mismo_numero": "#854D0E",
        "ola": "#3B82F6",
        "pista": "#16A34A",
        "destello": "#15803D",
    },
}


def mezclar_colores(color_a, color_b, factor):
    """Mezcla dos colores hexadecimales según un factor entre 0 y 1.

    Args:
        color_a (str): Color inicial, por ejemplo "#FFFFFF".
        color_b (str): Color final, por ejemplo "#000000".
        factor (float): 0 devuelve color_a y 1 devuelve color_b.

    Returns:
        str: Color resultante en formato hexadecimal.
    """
    canales_a = [int(color_a[i : i + 2], 16) for i in (1, 3, 5)]
    canales_b = [int(color_b[i : i + 2], 16) for i in (1, 3, 5)]
    mezcla = [round(a + (b - a) * factor) for a, b in zip(canales_a, canales_b)]
    return f"#{mezcla[0]:02X}{mezcla[1]:02X}{mezcla[2]:02X}"


class BotonRedondeado(tk.Canvas):
    """Botón con esquinas redondeadas, efecto hover y efecto de presionado."""

    def __init__(
        self, padre, texto, color, comando, fondo, ancho=120, alto=40, fuente=None
    ):
        """Crea el botón y registra los eventos del mouse.

        Args:
            padre: Widget contenedor del botón.
            texto (str): Texto que muestra el botón.
            color (str): Color de fondo del botón en formato hexadecimal.
            comando: Función que se ejecuta al hacer clic.
            fondo (str): Color del contenedor, para que las esquinas encajen.
            ancho (int): Ancho solicitado en píxeles.
            alto (int): Alto del botón en píxeles.
            fuente (tuple): Fuente del texto; por defecto Helvetica 11 negrita.
        """
        super().__init__(
            padre,
            width=ancho,
            height=alto,
            bg=fondo,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.texto = texto
        self.color = color
        self.comando = comando
        self.fuente = fuente or (FUENTE, 11, "bold")
        self.estado = "normal"
        self.bind("<Configure>", self._dibujar)
        self.bind("<Enter>", self._al_entrar)
        self.bind("<Leave>", self._al_salir)
        self.bind("<ButtonPress-1>", self._al_presionar)
        self.bind("<ButtonRelease-1>", self._al_soltar)

    def _rectangulo_redondeado(self, x1, y1, x2, y2, radio, color):
        """Dibuja un rectángulo con esquinas redondeadas.

        Args:
            x1 (int): Coordenada x de la esquina superior izquierda.
            y1 (int): Coordenada y de la esquina superior izquierda.
            x2 (int): Coordenada x de la esquina inferior derecha.
            y2 (int): Coordenada y de la esquina inferior derecha.
            radio (int): Radio de las esquinas en píxeles.
            color (str): Color de relleno en formato hexadecimal.
        """
        puntos = [
            x1 + radio, y1, x1 + radio, y1,
            x2 - radio, y1, x2 - radio, y1,
            x2, y1, x2, y1 + radio,
            x2, y1 + radio, x2, y2 - radio,
            x2, y2 - radio, x2, y2,
            x2 - radio, y2, x2 - radio, y2,
            x1 + radio, y2, x1 + radio, y2,
            x1, y2, x1, y2 - radio,
            x1, y2 - radio, x1, y1 + radio,
            x1, y1 + radio, x1, y1,
        ]  # fmt: skip
        self.create_polygon(puntos, smooth=True, fill=color, outline=color)

    def _dibujar(self, event=None):
        """Redibuja el botón según su estado actual.

        Args:
            event: Evento de Tkinter que provocó el redibujado, si existe.
        """
        if not self.winfo_exists():
            return
        ancho = self.winfo_width()
        alto = self.winfo_height()
        if ancho <= 1:
            return

        color = self.color
        desplazamiento = 0
        if self.estado == "hover":
            color = mezclar_colores(self.color, "#000000", 0.12)
        elif self.estado == "presionado":
            color = mezclar_colores(self.color, "#000000", 0.25)
            desplazamiento = 1

        self.delete("all")
        self._rectangulo_redondeado(
            1, 1 + desplazamiento, ancho - 1, alto - 1, 12, color
        )
        self.create_text(
            ancho / 2,
            alto / 2 + desplazamiento,
            text=self.texto,
            fill="white",
            font=self.fuente,
        )

    def _al_entrar(self, event):
        """Aplica el efecto hover cuando el mouse entra al botón.

        Args:
            event: Evento <Enter> de Tkinter.
        """
        self.estado = "hover"
        self._dibujar()

    def _al_salir(self, event):
        """Quita el efecto hover cuando el mouse sale del botón.

        Args:
            event: Evento <Leave> de Tkinter.
        """
        self.estado = "normal"
        self._dibujar()

    def _al_presionar(self, event):
        """Aplica el efecto de hundido al presionar el botón.

        Args:
            event: Evento <ButtonPress-1> de Tkinter.
        """
        self.estado = "presionado"
        self._dibujar()

    def _al_soltar(self, event):
        """Ejecuta el comando si el clic se soltó dentro del botón.

        Args:
            event: Evento <ButtonRelease-1> de Tkinter.
        """
        dentro = (
            0 <= event.x <= self.winfo_width() and 0 <= event.y <= self.winfo_height()
        )
        self.estado = "hover" if dentro else "normal"
        self._dibujar()
        if dentro and self.comando is not None:
            self.comando()


class SudokuView(tk.Tk):
    """Gestor de la interfaz gráfica del juego Sudoku basada en Tkinter."""

    def __init__(self, controlador):
        """Inicializa la ventana principal de la aplicación y sus propiedades.

        Args:
            controlador: Objeto controlador que maneja la lógica de eventos.
        """
        super().__init__()
        self.controlador = controlador
        self.tema = "claro"
        self.title("Sudoku Clásico - Python GUI")
        self.geometry("520x700")
        self.resizable(False, False)
        self._ciclo = 0
        self.celdas_ui = {}
        self.celdas_fijas = set()
        self.celdas_error = set()
        self.celda_activa = None
        self._ocultas = set()
        self._colores_temporales = {}
        self._unidades_completas = set()
        self._animar_entrada = False
        self.lienzos_notas = {}
        self.boton_borrador = None
        self._teclas_borrador = set()
        self._lado_celda = 0
        self._celebracion = None
        self.crear_interfaz_menu()

    @property
    def paleta(self):
        """Devuelve el diccionario de colores del tema activo.

        Returns:
            dict: Colores del tema "claro" u "oscuro".
        """
        return PALETAS[self.tema]

    @property
    def modo_borrador(self):
        """Indica si el modo borrador está activo (el estado vive en el controlador).

        Returns:
            bool: True si las teclas numéricas anotan candidatos.
        """
        return self.controlador.modo_borrador

    def limpiar_ventana(self):
        """Elimina los widgets de la ventana y reinicia el estado del tablero.

        Incrementa el ciclo de pantalla para cancelar las animaciones
        pendientes de la pantalla anterior.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(bg=self.paleta["fondo"])
        self._ciclo += 1
        self.celdas_ui = {}
        self.celdas_fijas = set()
        self.celdas_error = set()
        self.celda_activa = None
        self._ocultas = set()
        self._colores_temporales = {}
        self._unidades_completas = set()
        self._animar_entrada = False
        self.lienzos_notas = {}
        self.boton_borrador = None
        self._teclas_borrador = set()
        self._celebracion = None

    def volver_menu(self):
        """Detiene la partida en curso y regresa al menú principal."""
        self.controlador.partida_activa = False
        self.crear_interfaz_menu()

    def alternar_tema(self):
        """Cambia entre el tema claro y oscuro conservando los datos del menú."""
        nombre = self.entry_jugador.get()
        dificultad = self.var_dificultad.get()
        self.tema = "oscuro" if self.tema == "claro" else "claro"
        self.crear_interfaz_menu()
        self.entry_jugador.delete(0, tk.END)
        self.entry_jugador.insert(0, nombre)
        self.var_dificultad.set(dificultad)

    def _despues(self, ms, funcion, *args):
        """Programa una función que se omite si la pantalla ya cambió.

        Args:
            ms (int): Milisegundos de espera antes de ejecutar la función.
            funcion: Función a ejecutar.
            *args: Argumentos que recibe la función.
        """
        self.after(ms, self._ejecutar_vigente, self._ciclo, funcion, args)

    def _ejecutar_vigente(self, ciclo, funcion, args):
        """Ejecuta la función solo si pertenece a la pantalla actual.

        Args:
            ciclo (int): Ciclo de pantalla en el que se programó la función.
            funcion: Función a ejecutar.
            args (tuple): Argumentos de la función.
        """
        if ciclo == self._ciclo:
            funcion(*args)

    def _limpiar_nombre_inicial(self, event):
        """Borra el texto de ejemplo del campo de nombre al enfocarlo.

        Args:
            event: Evento de foco de Tkinter (<FocusIn>).
        """
        if self.entry_jugador.get() == "Tu Nombre":
            self.entry_jugador.delete(0, tk.END)

    def _crear_boton(
        self, padre, texto, color, comando, fondo, ancho=220, alto=40, tamano=11
    ):
        """Crea un botón redondeado con el estilo visual de la aplicación.

        Args:
            padre: Widget contenedor del botón.
            texto (str): Texto que muestra el botón.
            color (str): Color de fondo del botón en formato hexadecimal.
            comando: Función que se ejecuta al presionar el botón.
            fondo (str): Color del contenedor, para que las esquinas encajen.
            ancho (int): Ancho solicitado en píxeles.
            alto (int): Alto del botón en píxeles.
            tamano (int): Tamaño de la fuente del texto.

        Returns:
            BotonRedondeado: El botón creado.
        """
        return BotonRedondeado(
            padre,
            texto,
            color,
            comando,
            fondo,
            ancho=ancho,
            alto=alto,
            fuente=(FUENTE, tamano, "bold"),
        )

    def crear_interfaz_menu(self):
        """Construye y despliega la pantalla del menú principal."""
        self.limpiar_ventana()
        p = self.paleta

        frame_menu = tk.Frame(self, padx=30, pady=20, bg=p["fondo"])
        frame_menu.pack(expand=True, fill="both")

        frame_tema = tk.Frame(frame_menu, bg=p["fondo"])
        frame_tema.pack(fill="x")
        texto_tema = "Modo oscuro" if self.tema == "claro" else "Modo claro"
        self._crear_boton(
            frame_tema,
            texto_tema,
            p["boton_neutro"],
            self.alternar_tema,
            p["fondo"],
            ancho=130,
            alto=32,
            tamano=10,
        ).pack(side="right")

        lbl_titulo = tk.Label(
            frame_menu,
            text="SUDOKU",
            font=(FUENTE, 36, "bold"),
            fg=p["titulo"],
            bg=p["fondo"],
        )
        lbl_titulo.pack(pady=(10, 0))

        lbl_subtitulo = tk.Label(
            frame_menu,
            text="Clásico · Python GUI",
            font=(FUENTE, 11),
            fg=p["subtexto"],
            bg=p["fondo"],
        )
        lbl_subtitulo.pack(pady=(0, 20))

        tarjeta = tk.Frame(
            frame_menu,
            bg=p["tarjeta"],
            padx=30,
            pady=25,
            highlightbackground=p["borde"],
            highlightthickness=1,
        )
        tarjeta.pack(fill="x", padx=20)

        lbl_user = tk.Label(
            tarjeta,
            text="Nombre del jugador",
            font=(FUENTE, 10, "bold"),
            fg=p["texto"],
            bg=p["tarjeta"],
        )
        lbl_user.pack(anchor="w")

        self.entry_jugador = tk.Entry(
            tarjeta,
            font=(FUENTE, 12),
            justify="center",
            relief="flat",
            bg=p["entrada"],
            fg=p["texto"],
            insertbackground=p["texto"],
            highlightthickness=1,
            highlightbackground=p["borde"],
            highlightcolor=p["acento"],
        )
        self.entry_jugador.pack(fill="x", pady=(4, 15), ipady=6)
        self.entry_jugador.insert(0, "Tu Nombre")
        self.entry_jugador.bind("<FocusIn>", self._limpiar_nombre_inicial)

        lbl_dif = tk.Label(
            tarjeta,
            text="Dificultad",
            font=(FUENTE, 10, "bold"),
            fg=p["texto"],
            bg=p["tarjeta"],
        )
        lbl_dif.pack(anchor="w")

        self.var_dificultad = tk.StringVar(value="Fácil")
        frame_radios = tk.Frame(tarjeta, bg=p["tarjeta"])
        frame_radios.pack(fill="x", pady=(4, 20))
        for dif in ["Fácil", "Medio", "Difícil"]:
            tk.Radiobutton(
                frame_radios,
                text=dif,
                variable=self.var_dificultad,
                value=dif,
                indicatoron=False,
                font=(FUENTE, 10, "bold"),
                bg=p["entrada"],
                fg=p["texto"],
                selectcolor=p["seleccion"],
                activebackground=p["borde"],
                activeforeground=p["texto"],
                relief="flat",
                bd=0,
                cursor="hand2",
                pady=6,
            ).pack(side="left", expand=True, fill="x", padx=2)

        botones_menu = [
            ("Nueva Partida", p["exito"], self.controlador.click_nueva_partida),
            ("Cargar Partida", p["acento"], self.controlador.cargar_partida),
            (
                "Ver Clasificación",
                p["secundario"],
                self.controlador.click_ver_clasificacion,
            ),
            (
                "Mis Estadísticas",
                p["secundario"],
                self.controlador.click_mis_estadisticas,
            ),
            ("Salir", p["peligro"], self.quit),
        ]
        for texto, color, comando in botones_menu:
            self._crear_boton(tarjeta, texto, color, comando, p["tarjeta"]).pack(
                fill="x", pady=4
            )

        lbl_devs = tk.Label(
            frame_menu,
            text="Desarrollado por: Alexander M., Noriel C., Deysi Q.",
            font=(FUENTE, 8, "italic"),
            fg=p["subtexto"],
            bg=p["fondo"],
        )
        lbl_devs.pack(side="bottom")

    def crear_interfaz_juego(self, nombre, dificultad):
        """Construye y visualiza el tablero interactivo y sus controles.

        Args:
            nombre (str): Nombre del jugador activo.
            dificultad (str): Nivel de dificultad seleccionado.
        """
        self.limpiar_ventana()
        self._animar_entrada = True
        p = self.paleta

        frame_header = tk.Frame(self, bg=p["encabezado"], pady=12)
        frame_header.pack(fill="x")

        lbl_info = tk.Label(
            frame_header,
            text=f"Jugador: {nombre}  |  Dificultad: {dificultad}",
            font=(FUENTE, 11, "bold"),
            fg="white",
            bg=p["encabezado"],
        )
        lbl_info.pack()

        frame_contadores = tk.Frame(
            self,
            bg=p["tarjeta"],
            pady=8,
            highlightbackground=p["borde"],
            highlightthickness=1,
        )
        frame_contadores.pack(pady=(15, 5))

        self.lbl_tiempo = tk.Label(
            frame_contadores,
            text="Tiempo: 00:00",
            font=(FUENTE, 11, "bold"),
            fg=p["titulo"],
            bg=p["tarjeta"],
            padx=15,
        )
        self.lbl_tiempo.pack(side="left")

        self.lbl_errores = tk.Label(
            frame_contadores,
            text="Errores: 0/5",
            font=(FUENTE, 11, "bold"),
            fg=p["peligro"],
            bg=p["tarjeta"],
            padx=15,
        )
        self.lbl_errores.pack(side="left")

        self.lbl_pistas = tk.Label(
            frame_contadores,
            text="Pistas: 0/3",
            font=(FUENTE, 11, "bold"),
            fg=p["exito"],
            bg=p["tarjeta"],
            padx=15,
        )
        self.lbl_pistas.pack(side="left")

        frame_tablero_borde = tk.Frame(
            self, bg=p["marco_tablero"], bd=0, padx=3, pady=3
        )
        frame_tablero_borde.pack(pady=10)

        vcmd = (self.register(self.validar_entrada_celda), "%P")
        fuente_celda = tkfont.Font(family=FUENTE, size=18, weight="bold")
        lado = fuente_celda.metrics("linespace") + 8
        self._lado_celda = lado

        for b_f in range(3):
            for b_c in range(3):
                subcuadrante = tk.Frame(frame_tablero_borde, bg=p["marco_tablero"])
                subcuadrante.grid(row=b_f, column=b_c, padx=1, pady=1)

                for f in range(3):
                    for c in range(3):
                        fila_real = b_f * 3 + f
                        col_real = b_c * 3 + c

                        marco = tk.Frame(
                            subcuadrante,
                            width=lado,
                            height=lado,
                            bg=p["borde"],
                        )
                        marco.grid(row=f, column=c)
                        marco.pack_propagate(False)

                        entry = tk.Entry(
                            marco,
                            width=1,
                            font=fuente_celda,
                            justify="center",
                            relief="flat",
                            bd=0,
                            bg=p["celda"],
                            fg=p["digito"],
                            insertbackground=p["texto"],
                            highlightthickness=1,
                            highlightbackground=p["borde"],
                            highlightcolor=p["acento"],
                            validate="key",
                            validatecommand=vcmd,
                        )
                        entry.pack(fill="both", expand=True)

                        entry.bind(
                            "<KeyRelease>",
                            lambda event, fila=fila_real, col=col_real: (
                                self._al_soltar_tecla(fila, col, event)
                            ),
                        )
                        entry.bind(
                            "<Button-1>",
                            lambda event, fila=fila_real, col=col_real: (
                                self._seleccionar_celda(fila, col)
                            ),
                        )
                        entry.bind(
                            "<FocusIn>",
                            lambda event, fila=fila_real, col=col_real: (
                                self._seleccionar_celda(fila, col)
                            ),
                        )
                        entry.bind(
                            "<KeyPress>",
                            lambda event, fila=fila_real, col=col_real: (
                                self._al_presionar_tecla(fila, col, event)
                            ),
                        )
                        self.celdas_ui[(fila_real, col_real)] = entry

                        lienzo = tk.Canvas(
                            marco,
                            width=lado,
                            height=lado,
                            bg=p["celda"],
                            highlightthickness=0,
                            bd=0,
                        )
                        lienzo.bind(
                            "<Button-1>",
                            lambda event, fila=fila_real, col=col_real: (
                                self._clic_notas(fila, col)
                            ),
                        )
                        self.lienzos_notas[(fila_real, col_real)] = lienzo

        frame_acciones = tk.Frame(self, bg=p["fondo"], pady=6)
        frame_acciones.pack()

        # Fila de ayudas: pista y modo borrador
        fila_ayudas = tk.Frame(frame_acciones, bg=p["fondo"])
        fila_ayudas.pack(pady=(0, 8))
        self._crear_boton(
            fila_ayudas,
            "Pedir Pista",
            p["exito"],
            self.controlador.click_pedir_pista,
            p["fondo"],
            ancho=235,
            alto=40,
        ).pack(side="left", padx=5)
        self.boton_borrador = self._crear_boton(
            fila_ayudas,
            "Borrador: OFF",
            p["boton_neutro"],
            self.alternar_borrador,
            p["fondo"],
            ancho=235,
            alto=40,
        )
        self.boton_borrador.pack(side="left", padx=5)

        # Fila de partida: guardar, auto-resolver y volver al menú
        fila_partida = tk.Frame(frame_acciones, bg=p["fondo"])
        fila_partida.pack()
        botones = [
            ("Guardar Partida", p["acento"], self.controlador.guardar_partida),
            ("Auto-Resolver", p["peligro"], self.controlador.click_auto_resolver),
            ("Menú Principal", p["secundario"], self.volver_menu),
        ]
        for texto, color, comando in botones:
            self._crear_boton(
                fila_partida,
                texto,
                color,
                comando,
                p["fondo"],
                ancho=150,
                alto=36,
                tamano=10,
            ).pack(side="left", padx=5)

    @staticmethod
    def _celdas_de_unidad(tipo, indice):
        """Devuelve las coordenadas de una fila, columna o bloque 3x3.

        Args:
            tipo (str): "f" para fila, "c" para columna o "b" para bloque.
            indice (int): Posición de la unidad, de 0 a 8.

        Returns:
            list[tuple[int, int]]: Las nueve coordenadas de la unidad.
        """
        if tipo == "f":
            return [(indice, c) for c in range(9)]
        if tipo == "c":
            return [(f, indice) for f in range(9)]
        base_f = 3 * (indice // 3)
        base_c = 3 * (indice % 3)
        return [(base_f + df, base_c + dc) for df in range(3) for dc in range(3)]

    def _valor_activo(self):
        """Devuelve el texto de la celda activa, o vacío si no hay ninguna.

        Returns:
            str: Contenido de la celda activa.
        """
        entry = self.celdas_ui.get(self.celda_activa)
        return entry.get() if entry is not None else ""

    def _color_natural(self, f, c, valor_activo):
        """Calcula el color de fondo de una celda sin animaciones.

        Args:
            f (int): Fila de la celda.
            c (int): Columna de la celda.
            valor_activo (str): Texto de la celda activa, vacío si no hay.

        Returns:
            str: Color de fondo en formato hexadecimal.
        """
        p = self.paleta
        if (f, c) in self.celdas_error:
            return p["error_fondo"]

        fija = (f, c) in self.celdas_fijas
        base = p["celda_fija"] if fija else p["celda"]
        activa = self.celda_activa
        if activa is None:
            return base
        if (f, c) == activa:
            return p["activa"]
        if valor_activo and self.celdas_ui[(f, c)].get() == valor_activo:
            return p["mismo_numero"]

        fila_a, col_a = activa
        mismo_bloque = f // 3 == fila_a // 3 and c // 3 == col_a // 3
        if f == fila_a or c == col_a or mismo_bloque:
            return p["fija_relacion"] if fija else p["relacion"]
        return base

    def _pintar_celda(self, f, c):
        """Aplica a una celda su color según selección, error o animación.

        Args:
            f (int): Fila de la celda.
            c (int): Columna de la celda.
        """
        entry = self.celdas_ui.get((f, c))
        if entry is None or not entry.winfo_exists():
            return
        p = self.paleta

        if (f, c) in self._ocultas:
            entry.config(
                bg=p["fondo"],
                disabledbackground=p["fondo"],
                fg=p["fondo"],
                disabledforeground=p["fondo"],
            )
            self._dibujar_notas(f, c, p["fondo"])
            return

        fondo = self._colores_temporales.get((f, c))
        if fondo is None:
            fondo = self._color_natural(f, c, self._valor_activo())
        texto = p["peligro"] if (f, c) in self.celdas_error else p["digito"]
        entry.config(
            bg=fondo,
            disabledbackground=fondo,
            fg=texto,
            disabledforeground=p["texto"],
        )
        self._dibujar_notas(f, c, fondo)

    def _repintar_tablero(self):
        """Aplica los colores de resaltado y de error a todas las celdas."""
        for f, c in list(self.celdas_ui):
            self._pintar_celda(f, c)

    def _seleccionar_celda(self, fila, col):
        """Marca una celda como activa y resalta las celdas relacionadas.

        Args:
            fila (int): Fila de la celda seleccionada.
            col (int): Columna de la celda seleccionada.
        """
        self.celda_activa = (fila, col)
        self._repintar_tablero()

    def _al_soltar_tecla(self, fila, col, event):
        """Reenvía al controlador solo las teclas que modifican una celda.

        Ignora flechas, Tab, Shift y otras teclas que no cambian el contenido,
        para que no se cuenten como movimientos del jugador.

        Args:
            fila (int): Fila de la celda donde se soltó la tecla.
            col (int): Columna de la celda donde se soltó la tecla.
            event: Evento de teclado de Tkinter (<KeyRelease>).
        """
        if event.keysym in self._teclas_borrador:
            self._teclas_borrador.discard(event.keysym)
            return
        if event.keysym in ("BackSpace", "Delete") or event.char.isdigit():
            self._despues(1, self._tras_modificar, fila, col)
            self.controlador.modificar_celda(fila, col, event)

    def _tras_modificar(self, fila, col):
        """Limpia el dígito temporal del borrador, repinta y revisa unidades.

        En modo borrador el controlador ya guardó la nota en el modelo, así
        que el dígito escrito en la celda se borra y solo queda la nota.

        Args:
            fila (int): Fila de la celda que se modificó.
            col (int): Columna de la celda que se modificó.
        """
        entry = self.celdas_ui.get((fila, col))
        if (
            self.controlador.modo_borrador
            and entry is not None
            and (fila, col) not in self.celdas_fijas
            and entry.get()
        ):
            entry.delete(0, tk.END)
        self._repintar_tablero()
        self._revisar_unidades(animar=True)

    def alternar_borrador(self):
        """Pide al controlador alternar el modo borrador y actualiza el botón."""
        activo = self.controlador.alternar_modo_borrador()
        p = self.paleta
        if self.boton_borrador is not None and self.boton_borrador.winfo_exists():
            self.boton_borrador.texto = "Borrador: ON" if activo else "Borrador: OFF"
            self.boton_borrador.color = p["acento"] if activo else p["boton_neutro"]
            self.boton_borrador._dibujar()
        entry = self.celdas_ui.get(self.celda_activa)
        if entry is not None:
            entry.focus_set()

    def _al_presionar_tecla(self, fila, col, event):
        """Protege las celdas con valor mientras el modo borrador está activo.

        En modo borrador, un dígito en una celda vacía pasa normal: al soltar
        la tecla el controlador lo guarda como nota. Pero si la celda ya tiene
        un valor (o se pulsa 0), la tecla se bloquea para no anotar ni borrar
        nada por accidente.

        Args:
            fila (int): Fila de la celda donde se presionó la tecla.
            col (int): Columna de la celda donde se presionó la tecla.
            event: Evento de teclado de Tkinter (<KeyPress>).

        Returns:
            str | None: "break" si la tecla se bloqueó.
        """
        celda = (fila, col)
        if not self.modo_borrador or celda in self.celdas_fijas:
            return None
        es_digito = len(event.char) == 1 and event.char.isdigit()
        if es_digito and (event.char == "0" or self.celdas_ui[celda].get()):
            self._teclas_borrador.add(event.keysym)
            return "break"
        return None

    def _clic_notas(self, fila, col):
        """Pasa el clic del lienzo de notas a la celda que cubre.

        Args:
            fila (int): Fila de la celda.
            col (int): Columna de la celda.
        """
        self.celdas_ui[(fila, col)].focus_set()
        self._seleccionar_celda(fila, col)

    def _dibujar_notas(self, f, c, fondo):
        """Dibuja las notas de una celda en una cuadrícula de 3x3.

        Las notas solo se muestran si la celda está vacía y visible.

        Args:
            f (int): Fila de la celda.
            c (int): Columna de la celda.
            fondo (str): Color de fondo actual de la celda.
        """
        lienzo = self.lienzos_notas.get((f, c))
        entry = self.celdas_ui.get((f, c))
        if lienzo is None or entry is None or not lienzo.winfo_exists():
            return
        notas = self.controlador.model.notas[f][c]
        if not notas or entry.get() or (f, c) in self._ocultas:
            lienzo.place_forget()
            return

        lienzo.config(bg=fondo)
        lienzo.delete("all")
        paso = self._lado_celda / 3
        for numero in sorted(notas):
            fila_n, col_n = divmod(numero - 1, 3)
            lienzo.create_text(
                (col_n + 0.5) * paso,
                (fila_n + 0.5) * paso,
                text=str(numero),
                fill=self.paleta["acento"],
                font=(FUENTE, 7, "bold"),
            )
        lienzo.place(x=0, y=0, relwidth=1, relheight=1)

    def _unidades_completas_ahora(self):
        """Calcula qué filas, columnas y bloques están completos y válidos.

        Returns:
            set[tuple[str, int]]: Pares (tipo, índice) de unidades completas.
        """
        completas = set()
        for tipo in ("f", "c", "b"):
            for indice in range(9):
                celdas = self._celdas_de_unidad(tipo, indice)
                textos = [self.celdas_ui[celda].get() for celda in celdas]
                sin_error = not any(celda in self.celdas_error for celda in celdas)
                if all(textos) and len(set(textos)) == 9 and sin_error:
                    completas.add((tipo, indice))
        return completas

    def _revisar_unidades(self, animar):
        """Detecta unidades recién completadas y hace destellar sus celdas.

        Args:
            animar (bool): Si es True, anima las unidades recién completadas.
        """
        if not self.celdas_ui:
            return
        actuales = self._unidades_completas_ahora()
        if animar:
            celdas = set()
            for tipo, indice in actuales - self._unidades_completas:
                celdas.update(self._celdas_de_unidad(tipo, indice))
            if celdas:
                self._desvanecer(celdas, self.paleta["destello"], pasos=10, ms=40)
        self._unidades_completas = actuales

    def _desvanecer(self, celdas, color_inicio, pasos=8, ms=45):
        """Anima un grupo de celdas desde un color hasta su color normal.

        Args:
            celdas (iterable): Coordenadas (fila, columna) de las celdas.
            color_inicio (str): Color con el que empieza la animación.
            pasos (int): Cantidad de pasos del desvanecimiento.
            ms (int): Milisegundos entre pasos.
        """
        self._paso_desvanecer(tuple(celdas), color_inicio, pasos, ms, 0)

    def _paso_desvanecer(self, celdas, color_inicio, pasos, ms, paso):
        """Ejecuta un paso del desvanecimiento y programa el siguiente.

        Args:
            celdas (tuple): Coordenadas de las celdas animadas.
            color_inicio (str): Color con el que empieza la animación.
            pasos (int): Cantidad total de pasos.
            ms (int): Milisegundos entre pasos.
            paso (int): Número del paso actual, desde 0.
        """
        if not self.celdas_ui:
            return
        valor_activo = self._valor_activo()
        for f, c in celdas:
            if paso >= pasos:
                self._colores_temporales.pop((f, c), None)
            else:
                natural = self._color_natural(f, c, valor_activo)
                self._colores_temporales[(f, c)] = mezclar_colores(
                    color_inicio, natural, paso / pasos
                )
            self._pintar_celda(f, c)
        if paso < pasos:
            self._despues(
                ms,
                self._paso_desvanecer,
                celdas,
                color_inicio,
                pasos,
                ms,
                paso + 1,
            )

    def _iniciar_ola(self):
        """Oculta el tablero y lo revela en diagonal, celda por celda."""
        self._ocultas = set(self.celdas_ui)
        self._repintar_tablero()
        for f, c in self.celdas_ui:
            self._despues((f + c) * 40, self._revelar_celda, f, c)

    def _revelar_celda(self, f, c):
        """Muestra una celda oculta con un destello que se desvanece.

        Args:
            f (int): Fila de la celda.
            c (int): Columna de la celda.
        """
        self._ocultas.discard((f, c))
        self._desvanecer({(f, c)}, self.paleta["ola"], pasos=4, ms=45)

    def _parpadear(self, celda, restantes):
        """Alterna el color de una celda con error para llamar la atención.

        Args:
            celda (tuple[int, int]): Coordenadas (fila, columna) de la celda.
            restantes (int): Cantidad de cambios de color que faltan.
        """
        entry = self.celdas_ui.get(celda)
        if entry is None or not entry.winfo_exists():
            return
        if restantes == 0:
            self._pintar_celda(*celda)
            return
        p = self.paleta
        color = p["parpadeo"] if restantes % 2 == 0 else p["error_fondo"]
        entry.config(bg=color)
        self._despues(110, self._parpadear, celda, restantes - 1)

    def mostrar_celebracion(
        self, resumen, al_terminar, duracion_ms=DURACION_CELEBRACION_MS
    ):
        """Muestra una animación de victoria con confeti y una frase aleatoria.

        Cubre toda la ventana, anima la frase, cuenta los puntos y, al
        terminar el tiempo (o al hacer clic), ejecuta la función indicada.

        Args:
            resumen (dict): Datos de la partida: jugador, dificultad, tiempo,
                errores, pistas y puntaje.
            al_terminar: Función sin argumentos que se llama al finalizar.
            duracion_ms (int): Duración total de la animación en milisegundos.
        """
        self.update_idletasks()
        ancho = self.winfo_width() if self.winfo_width() > 1 else 520
        alto = self.winfo_height() if self.winfo_height() > 1 else 700

        lienzo = tk.Canvas(
            self, bg=self.paleta["encabezado"], highlightthickness=0, bd=0
        )
        lienzo.place(x=0, y=0, relwidth=1, relheight=1)
        lienzo.focus_set()
        lienzo.bind("<Button-1>", lambda event: self._terminar_celebracion())

        cx = ancho / 2
        palabra = lienzo.create_text(
            cx,
            alto * 0.32,
            text=random.choice(PALABRAS_VICTORIA),
            fill="white",
            font=(FUENTE, -14, "bold"),
        )
        lienzo.create_text(
            cx,
            alto * 0.45,
            text=f"{resumen['jugador']}, completaste el Sudoku ({resumen['dificultad']})",
            fill="#CBD5E1",
            font=(FUENTE, 12),
        )
        lienzo.create_text(
            cx,
            alto * 0.51,
            text=(
                f"Tiempo {resumen['tiempo']}   ·   Errores {resumen['errores']}"
                f"   ·   Pistas {resumen['pistas']}"
            ),
            fill="#CBD5E1",
            font=(FUENTE, 11),
        )
        puntos = lienzo.create_text(
            cx,
            alto * 0.62,
            text="+0 pts",
            fill="#FBBF24",
            font=(FUENTE, 28, "bold"),
        )
        cuenta = lienzo.create_text(
            cx, alto - 30, text="", fill="#94A3B8", font=(FUENTE, 10)
        )

        self._celebracion = {
            "lienzo": lienzo,
            "ancho": ancho,
            "alto": alto,
            "inicio": time.monotonic(),
            "duracion": duracion_ms,
            "palabra": palabra,
            "puntos": puntos,
            "cuenta": cuenta,
            "puntaje": resumen["puntaje"],
            "particulas": [],
            "al_terminar": al_terminar,
        }
        # Dos cañones de confeti desde las esquinas inferiores
        for _ in range(45):
            self._nueva_particula(
                ancho * 0.05, alto, random.uniform(2, 9), -random.uniform(11, 18)
            )
            self._nueva_particula(
                ancho * 0.95, alto, -random.uniform(2, 9), -random.uniform(11, 18)
            )
        self._paso_celebracion()

    def _nueva_particula(self, x, y, vx, vy):
        """Crea una pieza de confeti en el lienzo de la celebración.

        Args:
            x (float): Posición horizontal inicial.
            y (float): Posición vertical inicial.
            vx (float): Velocidad horizontal inicial.
            vy (float): Velocidad vertical inicial.
        """
        est = self._celebracion
        lienzo = est["lienzo"]
        ancho_p = random.randint(5, 10)
        alto_p = random.randint(4, 8)
        crear = lienzo.create_oval if random.random() < 0.3 else lienzo.create_rectangle
        item = crear(
            x,
            y,
            x + ancho_p,
            y + alto_p,
            fill=random.choice(COLORES_CONFETI),
            outline="",
        )
        lienzo.tag_lower(item)
        est["particulas"].append(
            [item, x, y, vx, vy, ancho_p, alto_p, random.uniform(0, 6.28)]
        )

    def _paso_celebracion(self):
        """Dibuja un cuadro de la celebración y programa el siguiente."""
        est = self._celebracion
        if est is None or not est["lienzo"].winfo_exists():
            return
        lienzo = est["lienzo"]
        t = (time.monotonic() - est["inicio"]) * 1000
        if t >= est["duracion"]:
            self._terminar_celebracion()
            return

        # Frase: entra creciendo con rebote y luego "late" cambiando de color
        k = min(1.0, t / 700)
        c1 = 1.70158
        c3 = c1 + 1
        suavizado = 1 + c3 * (k - 1) ** 3 + c1 * (k - 1) ** 2
        tam = 14 + 28 * suavizado
        if k >= 1:
            tam = 42 + 2 * math.sin(t / 140)
        lienzo.itemconfig(
            est["palabra"],
            font=(FUENTE, -round(tam), "bold"),
            fill=COLORES_CONFETI[int(t / 160) % len(COLORES_CONFETI)],
        )

        # Puntaje que sube de 0 hasta el valor final
        avance = min(1.0, max(0.0, (t - 600) / 1400))
        lienzo.itemconfig(
            est["puntos"], text=f"+{int(est['puntaje'] * avance)} pts"
        )

        restante = math.ceil((est["duracion"] - t) / 1000)
        lienzo.itemconfig(
            est["cuenta"],
            text=f"Volviendo al menú en {restante}…  (clic para saltar)",
        )

        # Lluvia de confeti hasta poco antes del final
        if t < est["duracion"] - 1200:
            for _ in range(2):
                self._nueva_particula(
                    random.uniform(0, est["ancho"]),
                    -10,
                    random.uniform(-1, 1),
                    random.uniform(1.5, 3.5),
                )

        vivas = []
        for part in est["particulas"]:
            item, x, y, vx, vy, ancho_p, alto_p, fase = part
            vy = min(vy + 0.3, 6)
            vx *= 0.99
            x += vx + math.sin(fase + t / 200) * 0.8
            y += vy
            if y > est["alto"] + 20:
                lienzo.delete(item)
                continue
            lienzo.coords(item, x, y, x + ancho_p, y + alto_p)
            part[1:5] = [x, y, vx, vy]
            vivas.append(part)
        est["particulas"] = vivas

        self._despues(33, self._paso_celebracion)

    def _terminar_celebracion(self):
        """Cierra la celebración (una sola vez) y ejecuta la acción final."""
        est = self._celebracion
        if est is None:
            return
        self._celebracion = None
        if est["al_terminar"] is not None:
            est["al_terminar"]()
        elif est["lienzo"].winfo_exists():
            est["lienzo"].destroy()

    def validar_entrada_celda(self, texto):
        """Valida que la celda quede vacía o con un dígito del 1 al 9.

        Args:
            texto (str): Cadena enviada por el evento de validación.

        Returns:
            bool: True si el texto es válido para la entrada, False si no.
        """
        return texto == "" or (len(texto) == 1 and texto in "123456789")

    def actualizar_tablero_interfaz(self, matriz_juego, matriz_pistas):
        """Sincroniza valores y estado bloqueado de las celdas en pantalla.

        Si es la primera actualización de una partida, anima la entrada en
        ola. Si aparecen celdas fijas nuevas (pistas), las anima en verde.

        Args:
            matriz_juego (list[list[int]]): Estado actual del tablero.
            matriz_pistas (list[list[bool]]): Celdas iniciales o de pista.
        """
        anteriores = set(self.celdas_fijas)
        self.celdas_fijas = set()
        self.celdas_error = set()
        for (f, c), entry in self.celdas_ui.items():
            entry.config(state="normal")
            valor = matriz_juego[f][c]
            entry.delete(0, tk.END)
            if valor != 0:
                entry.insert(0, str(valor))

            if matriz_pistas[f][c]:
                self.celdas_fijas.add((f, c))
                entry.config(state="disabled")

        if self._animar_entrada:
            self._animar_entrada = False
            self._unidades_completas = self._unidades_completas_ahora()
            self._iniciar_ola()
            return

        self._repintar_tablero()
        nuevas = self.celdas_fijas - anteriores
        if nuevas:
            self._revisar_unidades(animar=True)
            self._desvanecer(nuevas, self.paleta["pista"], pasos=12, ms=55)
        else:
            self._revisar_unidades(animar=False)

    def mostrar_error_celda(self, f, c):
        """Resalta en rojo una celda en conflicto y la hace parpadear.

        Args:
            f (int): Fila de la celda.
            c (int): Columna de la celda.
        """
        self.celdas_error.add((f, c))
        self._repintar_tablero()
        self._parpadear((f, c), 6)

    def limpiar_error_celda(self, f, c):
        """Restablece el estilo normal de una celda marcada con error.

        Args:
            f (int): Fila de la celda.
            c (int): Columna de la celda.
        """
        self.celdas_error.discard((f, c))
        self._repintar_tablero()