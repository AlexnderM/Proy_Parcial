# Organizador automatico de archivos
Este proyecto consiste en una herramienta de automatización en Python diseñada para escanear una carpeta específica y clasificar sus archivos en subcarpetas organizadas según el tipo o extensión del archivo.

## Desarrolladores del proyecto
Alexander Madrid
Noriel Cortes
Deysi Quintero

## Especificaciones del proyecto
El script procesa únicamente archivos sueltos en el directorio raíz configurado, omitiendo carpetas existentes para evitar bucles o alteraciones en la estructura interna de otros proyectos. Utiliza exclusivamente módulos nativos de Python, asegurando una ejecución ligera sin dependencias externas.

### Categorias de Organización por Defecto
* *Documentos:* '.pdf', '.docx', '.doc', '.txt', '.xlsx', 'pptx', '.csv'
* *Imágenes:* '.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp'
* *Audio:* '.mp3', '.wav', '.m4a', '.flac'
* *Videos:* '.mp4', '.mkv', '.mov', '.avi'
* *Archivos Comprimidos:* '.zip', '.rar', '.tar', '.gz'

## Requisitos Funcionales
* *Lectura de ruta:* El sistema debe permitir especificar o configurar la ruta de la carpeta que se desea organizar.
* *Identificación de extensiones:* El programa debe leer la extensión de cada archivo presente en el directorio configurado de forma precisa.
* *Clasificación por categorías:* El sistema debe asociar cada extensión detectada con su grupo lógico correspondiente (ej. Imágenes, Documentos).
* *Creación automática de carpetas:* El programa debe verificar si las carpetas de destino existen; si no, debe crearlas automáticamente antes de mover los archivos.
* *Transferencia de archivos:* El script debe mover de forma segura cada archivo desde la carpeta origen hacia su carpeta destino sin corromper el contenido.
* *Control de duplicados:* Si un archivo con el mismo nombre ya existe en el destino, el sistema debe renombrar el nuevo archivo añadiendo un sufijo numérico (ej. 'archivo(1).pdf') para evitar la pérdida de datos por sobrescritura.
* *Ignorar subcarpetas:* El script debe procesar únicamente archivos sueltos e ignorar las subcarpetas ya existentes en el directorio de origen.
* *Reporte de ejecución:* Al finalizar, el programa debe mostrar un resumen en la consola indicando la cantidad total de archivos organizados con éxito.

## Tecnologías y Requisitos del Entorno
* *Lenguaje:* Python 3.14
* *Librerías Estándar (No requieren instalación externa):*
  * 'os': Para manipular rutas, listar directorios y crear carpetas, conectando el código con el sistema operativo.
  * 'shutil': Para transferir, mover archivos y comprimir carpetas enteras.
