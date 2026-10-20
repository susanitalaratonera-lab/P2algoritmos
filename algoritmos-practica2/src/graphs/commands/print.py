"""Comando do intérprete para mostrar a estrutura do grafo por pantalla."""

from __future__ import annotations

import typing
import builtins
from graphs import Graph


def print(graph: Graph | None) -> Graph:
    """Imprime a estrutura actual do grafo (matriz de adxacencia e vértices).

    Comportamiento:
        - Involucra o método de representación do grafo en consola.
        - Non altera o estado do grafo.

    Sintaxis en el script:
        PRINT

    Args:
        graph (Graph | None): Grafo actual en memoria.

    Returns:
        Graph: O mesmo grafo sen modificacións.

    Raises:
        ValueError: Se o grafo é None.
    """
    if graph is None:
        builtins.print("NO GRAPH FOUND")
        return graph

    # `builtins.print` é o print de Python (esta función tapa o nome `print`)
    builtins.print("GRAPH CONTENT:")
    builtins.print(graph)
    return graph