import pprint
import sys
import traceback
from typing import List

import cuatro_en_linea

# Si las pruebas se ven mal en tu terminal, probá cambiando el valor
# de esta constante a True para desactivar los colores ANSI.
TERMINAL_SIN_COLOR = False


def validar_estado(desc: List[List[str]], tablero: List[List[str]]):
    """Asegura que `tablero` tenga un estado similar a `desc`. Se prueba que:
    - El tipo de cada elemento, en todos sus niveles, sea el mismo
    - Las dimensiones sean las mismas
    - El contenido sea el mismo
    """
    x = None
    y = None
    ancho, alto = len(desc[0]), len(desc)
    try:
        assert type(desc) is type(tablero), "Valor en `tablero` no es del tipo lista"
        assert len(tablero) > 0, "Lista en `tablero` está vacía"
        assert (ancho, alto) == (len(tablero[0]), len(tablero)), (
            f"Dimension obtenida ({len(tablero[0])}, {len(tablero)}) no es la esperada "
            f"({len(desc[0])}, {len(desc)})"
        )
        for y in range(alto):
            assert type(desc[y]) is type(
                tablero[y]
            ), f"Valor en `tablero[{y}]` no es del tipo lista"
            for x in range(ancho):
                assert type(desc[y][x]) is type(
                    tablero[y][x]
                ), f"Valor en `tablero[{y}][{x}]` no es del tipo string"
                assert desc[y][x] == tablero[y][x]
    except AssertionError as exc:
        error_msg = "Estado esperado:\n"
        error_msg += pprint.pformat(desc) + "\n\n"
        error_msg += "Estado actual:\n"
        error_msg += pprint.pformat(tablero) + "\n\n"
        if x is not None and y is not None:
            error_msg += f"Error en columna = {x}, fila = {y}:\n"
            error_msg += f"\tValor esperado: {desc[y][x]}\n"
            error_msg += f"\tValor encontrado: {tablero[y][x]}\n"
        raise AssertionError(error_msg + str(exc)) from exc


def test_01_crear_tablero_minimo_4x4():
    """Crea un nuevo tablero básico de Cuatro en línea de dimensiones 4x4."""
    desc = [
        [".", ".", ".", "."],
        [".", ".", ".", "."],
        [".", ".", ".", "."],
        [".", ".", ".", "."],
    ]
    tablero = cuatro_en_linea.crear_tablero(4, 4)
    validar_estado(desc, tablero)


def test_02_crear_tablero_rectangular():
    """Crea un nuevo tablero de Cuatro en línea de dimensiones 4x7."""
    desc = [
        [".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", "."],
    ]
    tablero = cuatro_en_linea.crear_tablero(4, 7)
    validar_estado(desc, tablero)


def test_03_colocar_x_en_columna_vacia():
    """Valida que colocar una ficha en columna vacía la ubique al fondo."""
    desc = [
        [".", ".", ".", "."],
        [".", ".", ".", "."],
        [".", ".", ".", "."],
        [".", "X", ".", "."],
    ]
    tablero = cuatro_en_linea.crear_tablero(4, 4)
    assert cuatro_en_linea.colocar_ficha(tablero, 1, "X"), (
        "Llamada válida a función de colocar con índice columna=1 devolvió `False`"
    )
    validar_estado(desc, tablero)


def test_04_apilar_segunda_ficha_misma_columna():
    """Valida apilar dos fichas en la misma columna."""
    desc = [
        [".", ".", ".", "."],
        [".", ".", ".", "."],
        [".", "O", ".", "."],
        [".", "X", ".", "."],
    ]
    tablero = cuatro_en_linea.crear_tablero(4, 4)
    assert cuatro_en_linea.colocar_ficha(tablero, 1, "X")
    assert cuatro_en_linea.colocar_ficha(tablero, 1, "O")
    validar_estado(desc, tablero)


def test_05_columna_negativa_devuelve_false():
    """Asegura que no se pueda jugar en una columna negativa."""
    desc = cuatro_en_linea.crear_tablero(4, 4)
    tablero = cuatro_en_linea.crear_tablero(4, 4)
    assert not cuatro_en_linea.colocar_ficha(tablero, -1, "X"), (
        "Llamada inválida a función de colocar con índice columna=-1 devolvió `True`"
    )
    validar_estado(desc, tablero)


def test_06_columna_fuera_de_rango_devuelve_false():
    """Asegura que no se pueda jugar en una columna fuera de rango."""
    desc = cuatro_en_linea.crear_tablero(4, 4)
    tablero = cuatro_en_linea.crear_tablero(4, 4)
    assert not cuatro_en_linea.colocar_ficha(tablero, 4, "X"), (
        "Llamada inválida a función de colocar con índice columna=4 devolvió `True`"
    )
    validar_estado(desc, tablero)


def test_07_columna_llena_devuelve_false():
    """Asegura que no se pueda jugar en una columna llena."""
    desc = [
        [".", ".", "O", "."],
        [".", ".", "X", "."],
        [".", ".", "O", "."],
        [".", ".", "X", "."],
    ]
    tablero = cuatro_en_linea.crear_tablero(4, 4)
    assert cuatro_en_linea.colocar_ficha(tablero, 2, "X")
    assert cuatro_en_linea.colocar_ficha(tablero, 2, "O")
    assert cuatro_en_linea.colocar_ficha(tablero, 2, "X")
    assert cuatro_en_linea.colocar_ficha(tablero, 2, "O")
    assert not cuatro_en_linea.colocar_ficha(tablero, 2, "X"), (
        "Llamada inválida a función de colocar en columna llena devolvió `True`"
    )
    validar_estado(desc, tablero)


def test_08_ganador_horizontal_simple():
    """Verifica un caso simple de victoria horizontal."""
    tablero = [
        [".", ".", ".", ".", "."],
        [".", ".", ".", ".", "."],
        [".", ".", ".", ".", "."],
        ["X", "X", "X", "X", "."],
    ]
    assert cuatro_en_linea.hay_ganador(tablero, "X"), (
        "`hay_ganador` devolvió `False` para una línea horizontal válida"
    )


def test_09_ganador_vertical_simple():
    """Verifica un caso simple de victoria vertical."""
    tablero = [
        [".", ".", "O", "."],
        [".", ".", "O", "."],
        [".", ".", "O", "."],
        [".", ".", "O", "."],
    ]
    assert cuatro_en_linea.hay_ganador(tablero, "O"), (
        "`hay_ganador` devolvió `False` para una línea vertical válida"
    )


def test_10_tablero_recien_creado_no_esta_lleno():
    """Verifica que un tablero recién creado no esté lleno."""
    tablero = cuatro_en_linea.crear_tablero(4, 4)
    assert not cuatro_en_linea.esta_lleno(tablero), (
        "`esta_lleno` devolvió `True` para un tablero recién creado"
    )


# Sólo se van a correr aquellos tests que estén mencionados dentro de la
# siguiente constante
TESTS = (
    test_01_crear_tablero_minimo_4x4,
    test_02_crear_tablero_rectangular,
    test_03_colocar_x_en_columna_vacia,
    test_04_apilar_segunda_ficha_misma_columna,
    test_05_columna_negativa_devuelve_false,
    test_06_columna_fuera_de_rango_devuelve_false,
    test_07_columna_llena_devuelve_false,
    test_08_ganador_horizontal_simple,
    test_09_ganador_vertical_simple,
    test_10_tablero_recien_creado_no_esta_lleno,
)

# El código que viene abajo tiene algunas *magias* para simplificar la corrida
# de los tests y proveer la mayor información posible sobre los errores que se
# produzcan. ¡No te preocupes si no lo entendés completamente!

# Colores ANSI para una salida más agradable en las terminales que lo permitan
COLOR_OK = "\033[1m\033[92m"
COLOR_ERR = "\033[1m\033[91m"
COLOR_RESET = "\033[0m"


def print_color(color: str, *args, **kwargs):
    """
    Mismo comportamiento que `print` pero con un
    primer parámetro para indicar de qué color se
    imprimirá el texto.

    Si la constante TERMINAL_SIN_COLOR es True,
    esta función será exactamente equivalente
    a utilizar `print`.
    """
    if TERMINAL_SIN_COLOR:
        print(*args, **kwargs)
    else:
        print(color, end="")
        print(*args, **kwargs)
        print(COLOR_RESET, end="", flush=True)


def main():
    tests_fallidos = []
    tests_a_correr = [int(t) for t in sys.argv[1:]]
    for i, test in [
        (i, test)
        for i, test in enumerate(TESTS)
        if not tests_a_correr or i + 1 in tests_a_correr
    ]:
        print(f"Prueba {i + 1 :02} - {test.__name__}: ", end="", flush=True)
        try:
            test()
            print_color(COLOR_OK, "[OK]")
        except AssertionError as e:
            tests_fallidos.append(test.__name__)
            print_color(COLOR_ERR, "[ERROR]")
            print_color(COLOR_ERR, " >", *e.args)
            break
        except Exception:
            tests_fallidos.append(test.__name__)
            print_color(COLOR_ERR, "[BOOM - Explotó]")
            print("\n--------------- Python dijo: ---------------")
            traceback.print_exc()
            print("--------------------------------------------\n")
            break

    if not tests_fallidos:
        print()
        print_color(COLOR_OK, "###########")
        print_color(COLOR_OK, "# TODO OK #")
        print_color(COLOR_OK, "###########")
        print()
    else:
        print()
        print_color(COLOR_ERR, "##################################")
        print_color(COLOR_ERR, "              ¡ERROR!             ")
        print_color(COLOR_ERR, "Falló el siguiente test:")
        for test_con_error in tests_fallidos:
            print_color(COLOR_ERR, " - " + test_con_error)
        print_color(COLOR_ERR, "##################################")
        print(
            "TIP: Si la información de arriba no es suficiente para entender "
            "el error, revisá el código de las pruebas que fallaron en el "
            "archivo cuatro_en_linea_test.py."
        )


main()
