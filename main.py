"""Módulo principal de entrada para la aplicación de Sudoku.

Inicializa el controlador del juego y arranca el bucle principal
de la interfaz de usuario.
"""

from sudoku.controller import SudokuController
from sudoku.model import SudokuModel
from sudoku.view import SudokuView


def main():
    """Punto de entrada principal que instancia y ejecuta la aplicación."""
    model = SudokuModel()
    controller = SudokuController(model, None)
    view = SudokuView(controlador=controller)
    controller.view = view
    
    view.mainloop()


if __name__ == "__main__":
    main()