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
    # TODO: [Práctica Alumno]
    # 1. Validar que o grafo non sexa None (lanzar ValueError en caso contrario).
    # 2. Obter o conxunto de compoñentes conexas mediante `graph.connected_components()`.
    # 3. Imprimir o número total de compoñentes e os nodos pertencentes a cada unha delas.
    # 4. Devolver o grafo orixinal.
    ...