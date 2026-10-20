"""Comando do intérprete para calcular as compoñentes conexas do grafo."""

from __future__ import annotations

import typing

from graphs import Graph


def components(graph: Graph | None) -> Graph:
    """Calcula e amosa as compoñentes conexas (ou fortemente conexas) do grafo.

    Comportamento:
        - Se o grafo é non dirixido, calcula as Compoñentes Conexas (CC).
        - Se o grafo é dirixido, calcula as Compoñentes Fortemente Conexas (SCC)
          usando a intersección de descendentes e ascendentes D(v) ∩ A(v).
        - Imprime cada compoñente identificada coa súa lista de nodos.

    Sintaxe no script:
        COMPONENTS

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
    if not graph.vertices:
        print("GRAPH IS EMPTY")
        return graph

    # Ordénanse os nodos de cada compoñente e as compoñentes entre si
    # para que a saída sexa sempre a mesma
    components = sorted(sorted(component) for component in graph.connected_components())
    sets = ", ".join(
        "{" + ", ".join(node.name for node in component) + "}" for component in components
    )
    print(f"CONNECTED COMPONENTS: [{sets}]")
    return graph