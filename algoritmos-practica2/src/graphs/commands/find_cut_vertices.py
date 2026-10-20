"""Comando do intérprete para atopar os vértices de corte (puntos de articulación)."""

from __future__ import annotations

import typing

from graphs import Graph


def find_cut_vertices(graph: Graph | None) -> Graph:
    """Calcula e amosa os vértices de corte (puntos de articulación ou puntos críticos de falla) do grafo.

    Comportamento:
        - Identifica aqueles nodos cuxa eliminación aumentaría o número de
          compoñentes conexas do grafo.
        - Imprime a lista de nodos críticos atopados por pantalla.

    Sintaxe no script:
        CUT_VERTICES

    Args:
        graph (Graph | None): Grafo actual en memoria.

    Returns:
        Graph: O grafo orixinal sen cambios.

    Raises:
        ValueError: Se o grafo é None.
    """
    # TODO: [Práctica Alumno]
    # 1. Validar que o grafo non sexa None (lanzar ValueError en caso contrario).
    # 2. Obter os vértices de corte chamando a `graph.find_cut_vertices()`.
    # 3. Formatear e imprimir os nomes dos nodos críticos atopados e a cantidade total.
    # 4. Devolver o grafo orixinal.
    ...