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
    # TODO: [Práctica Alumno]
    # 1. Validar que o grafo non sexa None (lanzar ValueError en caso contrario).
    # 2. Imprimir o grafo en consola (usar `builtins.print(graph)` para evitar conflitos co nome da función).
    # 3. Devolver o grafo sen modificacións.
    ...