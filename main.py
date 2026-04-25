"""
Interfaz e interacción con el usuario para el juego Cuatro en linea
"""

import cuatro_en_linea

PAD = 3


def pedir_entero(mensaje: str, minimo: int) -> int:
    """Solicita al usuario un número entero y valida la entrada.

    PRECONDICIONES:
        - `mensaje` es una cadena de texto que se muestra al usuario.
        - `minimo` es un entero positivo.

    POSTCONDICIONES:
        - La función devuelve un entero mayor o igual a `minimo`.
        - La función no retorna hasta que se ingrese un valor válido.
    """
    op = input(mensaje)
    while not op.lstrip("-").isdigit() or int(op) < minimo:
        op = input(f"Entrada inválida, vuelva a ingresar un entero >= {minimo}: ")
    return int(op)


def pedir_columna(mensaje: str) -> int:
    """Solicita al usuario una columna y valida solo que sea un entero.

    PRECONDICIONES:
        - `mensaje` es una cadena de texto que se muestra al usuario.

    POSTCONDICIONES:
        - Devuelve un entero ingresado por el usuario.
        - La función no retorna hasta que se ingrese un entero válido.
    """
    while True:
        op = input(mensaje)
        if op.lstrip("-").isdigit():
            return int(op)
        print("Entrada inválida, la columna debe ser un número entero.")


def mostrar_tablero(tablero: list[list[str]]) -> None:
    """Muestra el tablero del juego en formato tabular con índices.

    PRECONDICIONES:
        - `tablero` es una lista de listas de strings de cualquier dimensión.

    POSTCONDICIONES:
        - La función imprime el tablero en la consola.
        - No modifica el tablero original.
    """
    n_filas = len(tablero)
    n_columnas = len(tablero[0])

    indice_columnas = []
    for col in range(n_columnas):
        indice_columnas.append(str(col).center(PAD))

    print("\n" + " " * PAD + "|" + "|".join(indice_columnas))
    print(" " * PAD + "=" * n_columnas * (PAD + 1))

    for fil in range(n_filas):
        fila = []
        for col in range(n_columnas):
            fila.append(str(tablero[fil][col]).center(PAD))
        print(str(fil).center(PAD) + "‖" + "|".join(fila))


def alternar_jugador(jugador: str) -> str:
    """Devuelve la ficha del siguiente jugador."""
    if jugador == "X":
        return "O"
    return "X"


def main() -> None:
    """Función principal del juego Cuatro en línea.

    Ejecuta el flujo completo del juego: solicita dimensiones del tablero, crea
    el tablero inicial y permite jugar por turnos hasta victoria o empate.
    """
    print("=== Cuatro en línea ===")

    columnas = pedir_entero("Ingrese el ancho del juego (>= 4): ", 4)
    filas = pedir_entero("Ingrese el alto del juego (>= 4): ", 4)

    tablero = cuatro_en_linea.crear_tablero(filas, columnas)
    jugador = "X"

    mostrar_tablero(tablero)

    while not cuatro_en_linea.juego_terminado(tablero):
        print(f"Turno de {jugador}")
        columna = pedir_columna("Ingrese la columna a jugar: ")

        aplicado = cuatro_en_linea.colocar_ficha(tablero, columna, jugador)
        if not aplicado:
            if columna < 0 or columna >= columnas:
                print("Columna inválida.")
            else:
                print("La columna está llena.")
            continue

        mostrar_tablero(tablero)

        if not cuatro_en_linea.juego_terminado(tablero):
            jugador = alternar_jugador(jugador)

    if cuatro_en_linea.hay_ganador(tablero, "X"):
        print("Ganó X.")
    elif cuatro_en_linea.hay_ganador(tablero, "O"):
        print("Ganó O.")
    else:
        print("Empate: el tablero se llenó sin ganador.")


if __name__ == "__main__":
    main()
