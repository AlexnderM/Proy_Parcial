# Sudoku Clásico - Python GUI (MVC)

Aplicación interactiva de Sudoku desarrollada en Python utilizando Tkinter para la interfaz gráfica. El proyecto implementa una arquitectura Modelo-Vista-Controlador (MVC), algoritmos de Backtracking para la generación y resolución de tableros, y un flujo de Integración Continua (CI/CD) mediante GitHub Actions.

# Integrantes del Equipo

Alexander Madrid.

Noriel Cortés

Deysi Quintero.

# Características Principales

Arquitectura MVC: Separación clara entre la lógica del juego (model.py), la interfaz de usuario (view.py) y el flujo de control (controller.py), inicializados desde main.py.

Algoritmo de Backtracking: Generación aleatoria de soluciones válidas e integración de una función para resolver automáticamente el juego.

Niveles de Dificultad: Opciones de juego en niveles Fácil (40 celdas visibles), Medio (32 celdas visibles) y Difícil (25 celdas visibles).

Validación en Tiempo Real: Detección de conflictos en filas, columnas y subcuadrículas de 3x3 con marcas de error visuales y límite de 5 fallos.

Sistema de Ayudas: Hasta 3 pistas automáticas por partida.

Cronómetro y Puntuación: Registro de tiempo transcurrido y cálculo de puntaje en función de la dificultad, tiempo y errores cometidos.

Persistencia de Datos (JSON): Guardado automático de partidas completadas para la consulta de Top 10 (Clasificación) y Estadísticas Personales.

# Estructura del Proyecto

```text
Proy_Parcial/
├── .github/
│   └── workflows/
│       ├── ci.yml            # Workflow de pruebas y compilación
│       └── lint.yml          # Workflow de análisis de estilo con Ruff
├── docs/                     # Documentación adicional del proyecto
├── .env.example              # Ejemplo de variables de entorno
├── .gitignore                # Archivos ignorados por Git
├── controller.py             # Controlador: Maneja eventos e interactúa con Vista y Modelo
├── main.py                   # Punto de entrada principal para ejecutar la aplicación
├── model.py                  # Modelo: Lógica de negocio, Backtracking y persistencia JSON
├── view.py                   # Vista: Interfaz gráfica desarrollada con Tkinter
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Documentación general del proyecto
```


# Requisitos de Instalación

Python: Versión 3.10 o superior.

Tkinter: Generalmente incluido en las instalaciones estándar de Python para Windows y macOS.

# Ejecución del Proyecto

Clonar el repositorio:

git clone https://github.com/AlexnderM/Proy_Parcial.git
cd Proy_Parcial


Ejecutar la aplicación:
Ejecuta el archivo principal como punto de entrada:

python main.py


(En Windows, si la variable de entorno no está configurada en PowerShell, puedes usar py main.py o la ruta directa de tu ejecutable de Python).

# Integración Continua (CI/CD) y Calidad de Código

El repositorio cuenta con automatización en GitHub Actions para garantizar los estándares de calidad de software:

Sintaxis y Compilación (ci.yml): Valida que el proyecto no contenga errores de ejecución fundamentales en entornos de integración.

Análisis Estático de Código (lint.yml): Utiliza Ruff para forzar el cumplimiento de buenas prácticas de estilo en Python (PEP 8), manejo adecuado de zonas horarias (datetime.timezone), excepciones explícitas e importaciones limpias.

# Licencia

Proyecto desarrollado para fines académicos en la materia de Desarrollo de Software.
