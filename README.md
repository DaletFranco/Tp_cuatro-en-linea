# Cuatro en Línea - Python

Este es una implementación clásica del juego **Cuatro en Línea** desarrollada en Python. El proyecto cuenta con una separación clara entre la lógica del motor de juego, la interfaz de usuario por consola y una suite de pruebas para asegurar el correcto funcionamiento.

## 🚀 Características

* **Lógica Modular**: El motor del juego está separado de la interfaz.
* **Tablero Personalizable**: Permite jugar en tableros de diferentes dimensiones (mínimo 4x4).
* **Detección de Ganadores**: Algoritmo que verifica líneas horizontales, verticales y diagonales.
* **Pruebas Unitarias**: Incluye un archivo de tests para validar el comportamiento de las funciones principales.

## 🛠️ Estructura del Proyecto

* `cuatro_en_linea.py`: Contiene la lógica central (crear tablero, colocar fichas, verificar ganador).
* `main.py`: Interfaz de usuario y flujo principal de la partida.
* `cuatro_en_linea_test.py`: Suite de pruebas para verificar la integridad del código.

## 🎮 Cómo Jugar

1.  Asegúrate de tener instalado Python 3.
2.  Clona este repositorio o descarga los archivos.
3.  Ejecuta el archivo principal:
    ```bash
    python main.py
    ```
4.  Ingresa las dimensiones del tablero y sigue las instrucciones en pantalla para elegir las columnas.

## 🧪 Ejecución de Pruebas

Para validar que el motor del juego funciona correctamente, puedes ejecutar los tests incluidos:

```bash
python cuatro_en_linea_test.py
