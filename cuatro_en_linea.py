"""
Logica del juego Cuatro en linea
"""

Tablero = list[list[str]]

DIRECCIONES = [
    (0, 1),  # horizontal
    (1, 0),  # vertical
    (1, 1),  # diagonal descendente
    (-1, 1),  # diagonal ascendente
]


def crear_tablero(n_filas: int, n_columnas: int) -> Tablero:
    """Crea un tablero nuevo, con dimensiones `n_filas` por `n_columnas`.
    El tablero estará representado como una lista de listas de strings. Cada
    celda vacía se representa con ".", y las fichas de los jugadores se
    representan con "X" y "O".
    PRECONDICIONES:
        - `n_filas` y `n_columnas` son enteros mayores o iguales a cuatro.
    POSTCONDICIONES:
        - la función devuelve un nuevo tablero de strings que se puede utilizar
          para llamar al resto de las funciones del módulo.
        - todas las celdas del tablero devuelto valen ".".
    EJEMPLO:
        >>> crear_tablero(4, 5)
        [
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
            [".", ".", ".", ".", "."],
        ]
    """
    tablero = []  # es la lista vacía que va a contener las filas
    for _ in range(n_filas):  # tantas veces como filas...
        fila = [
            "." for _ in range(n_columnas)
        ]  # crea una lista de puntos que representan
        # una fila horizontal con  el ancho de las columnas especificadas en n_columnas
        tablero.append(fila)  # agrega la fila creada a la lista tablero
    return tablero  # devuelve la matriz completa


def colocar_ficha(tablero: Tablero, columna: int, ficha: str) -> bool:
    """Coloca la `ficha` en la `columna` indicada, respetando la caída por
    gravedad.
    Una jugada válida sobre una columna inserta la ficha en la posición libre
    más baja de esa columna.
    PRECONDICIONES:
        - `tablero` es una lista de listas de strings con formato válido.
        - `ficha` es "X" o "O".
    POSTCONDICIONES:
        - Si `columna` es válida y tiene espacio, la función modifica el tablero
        in-place y devuelve `True`.
        - Si `columna` es inválida (negativa o fuera de rango), no modifica el
        tablero y devuelve `False`.
        - Si la columna está llena, no modifica el tablero y devuelve `False`.
    EJEMPLO:
        >>> tablero = crear_tablero(4, 4)
        >>> colocar_ficha(tablero, 2, "X")
        True
        >>> tablero
        [
            [".", ".", ".", "."],
            [".", ".", ".", "."],
            [".", ".", ".", "."],
            [".", ".", "X", "."],
        ]"""
    filas = len(tablero)  # mide el tamaño del tablero para evitar errores de índice
    columnas = len(tablero[0])
    if (
        columna < 0 or columna >= columnas
    ):  # Valida si el número de columna ingresado existe.
        # Si no, devuelve False inmediatamente.
        return False
    for fila in range(filas - 1, -1, -1):  # Recorre las filas de abajo hacia arriba
        # (desde la última fila hasta la 0).
        if tablero[fila][columna] == ".":  # Pregunta: "¿Está vacío este lugar?".
            tablero[fila][
                columna
            ] = ficha  # Si está vacío, pone la ficha ("X" o "O") ahí.
            return True  # la jugada fue exitosa.
    return False  # la columna está llena.


def en_linea(
    tablero: Tablero, ficha: str, fila: int, col: int, direccion: tuple[int, int]
) -> bool:
    """Función auxiliar de hay_ganador.
    Verifica si hay cuatro fichas consecutivas
    desde una posición dada en una dirección específica.
    """
    df, dc = (
        direccion  # Desempaqueta la tupla de dirección, df es el cambio en fila, dc en columna.
    )
    for i in range(4):  # revisar 4 posiciones consecutivas (incluyendo la inicial).
        f = (
            fila + i * df
        )  # Calcula la coordenada de la ficha número i en la dirección dada.
        c = col + i * dc
        if not (0 <= f < len(tablero) and 0 <= c < len(tablero[0])):
            # que no se salga de los bordes del tablero
            return False
        if tablero[f][c] != ficha:
            # En los 4 pasos el programa mira qué hay en esa celda específica ([f][c]).
            # Si la ficha es igual: El inspector dice "Bien, esta es mía", y sigue
            # i la ficha es distinta (el !=), o sea, si encuentra un punto . o una ficha del rival O,
            # ya no hay posibilidad de que esa línea de 4 sea válida.
            return False

    return True


def hay_ganador_desde(tablero: Tablero, ficha: str, fila: int, col: int) -> bool:
    """Verifica si hay una secuencia ganadora desde una posición dada."""
    for direccion in DIRECCIONES:  # Itera sobre las 4 direcciones posibles
        if en_linea(
            tablero, ficha, fila, col, direccion
        ):  # Llama a la función anterior.
            # Si en alguna dirección hay 4, devuelve True
            return True
    return False


def hay_ganador(tablero: Tablero, ficha: str) -> bool:
    """Indica si `ficha` tiene al menos cuatro consecutivas en el tablero.

    La verificación contempla las cuatro direcciones válidas del juego:
    horizontal, vertical, diagonal descendente y diagonal ascendente.

    PRECONDICIONES:
        - `tablero` es una lista de listas de strings con formato válido.
        - `ficha` es "X" o "O".

    POSTCONDICIONES:
        - Devuelve True si existe una secuencia de cuatro o más fichas
          consecutivas de `ficha`.
        - Devuelve False en caso contrario.
        - No asume tablero cuadrado.
        - No evalúa posiciones fuera de rango.
    """
    for i_fila, fila in enumerate(tablero):  # para cada fila, lo que tenga adentro
        for i_col, celda in enumerate(fila):
            # para cada columna que cada fila tenga adentro que tenga una celda
            if celda == ficha and hay_ganador_desde(tablero, ficha, i_fila, i_col):
                # si es la mía entonces la cuento
                return True
    return False


def esta_lleno(tablero: Tablero) -> bool:
    """Indica si el tablero está lleno.
     PRECONDICIONES:
         - `tablero` es una lista de listas de strings con formato válido.
     POSTCONDICIONES:
         - Devuelve `True` si no queda ninguna celda ".".
         - Devuelve `False` si existe al menos una celda vacía.
    EJEMPLO:
        >>> tablero = [
         ...     ["X", "O", "X", "O"],
         ...     ["O", "X", "O", "X"],
         ...     ["X", "O", "X", "O"],
         ...     ["O", "X", "O", "X"],
         ... ]
         >>> esta_lleno(tablero)
         True"""

    for fila in tablero:
        for celda in fila:
            if celda == ".":  # si hay un punto el tablero no está lleno
                return False
    return True  # si recorre todo y no encontró puntos está lleno


def juego_terminado(tablero: Tablero) -> bool:
    """Indica si la partida terminó.
    La partida termina cuando gana "X", cuando gana "O" o cuando el tablero se
    llena. Si el tablero se llena sin ganador, la partida termina en empate.
    PRECONDICIONES:
        - `tablero` es una lista de listas de strings con formato válido.
    POSTCONDICIONES:
        - Devuelve `True` si hay un ganador o si el tablero está lleno.
        - Devuelve `False` si todavía puede jugarse otra jugada.

    EJEMPLO:
        >>> tablero = crear_tablero(4, 4)
        >>> juego_terminado(tablero)
        False
    """
    return hay_ganador(tablero, "X") or hay_ganador(tablero, "O") or esta_lleno(tablero)
