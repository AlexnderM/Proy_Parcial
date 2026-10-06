"""Módulo principal de entrada para la aplicación de Sudoku.

Inicializa el controlador del juego y arranca el bucle principal
de la interfaz de usuario.
"""

from controller import SudokuController


def main():
    """Punto de entrada principal que instancia y ejecuta la aplicación."""
    app = SudokuController()
    app.iniciar_aplicacion()


if __name__ == "__main__":
    main()