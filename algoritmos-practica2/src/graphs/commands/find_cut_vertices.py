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
    if graph is None:
        print("NO GRAPH FOUND")
        return graph

    try:
        cut_vertices = sorted(graph.find_cut_vertices())
    except RuntimeError:
        # So se definen para grafos non dirixidos (os de LOAD --power son dirixidos)
        print("CUT VERTICES ONLY AVAILABLE FOR UNDIRECTED GRAPHS")
        return graph
    names = ", ".join(node.name for node in cut_vertices)
    print(f"CUT VERTICES: [{names}]")
    return graph