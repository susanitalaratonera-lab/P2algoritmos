"""Comando do intérprete para calcular o camiño máis curto entre dous nodos."""

from __future__ import annotations

import typing

from graphs import Graph


def path(
    graph: Graph | None,
    origin_name: str,
    target_name: str,
) -> Graph:
    """Calcula o camiño máis curto entre dous nodos mediante o algoritmo de Dijkstra.

    Comportamiento:
        - Atopa a ruta de menor peso dende o nodo orixe ata o destino.
        - Imprime a secuencia de nodos que forman o camiño e o custo total acumulado.

    Sintaxe no script:
        PATH ISS SAT_1

    Args:
        graph (Graph | None): Grafo actual en memoria.
        origin_name (str): Nome do nodo orixe.
        target_name (str): Nome do nodo destino.

    Returns:
        Graph: O grafo orixinal sen cambios.

    Raises:
        ValueError: Se o grafo é None ou algún dos nodos non existe.
    """
    # TODO: [Práctica Alumno]
    # 1. Validar que o grafo non sexa None e que os nodos orixe e destino existan (usar `graph.find_by_name`).
    # 2. Executar o método `graph.path(origin_node, target_node)` para obter a ruta e o custo acumulado.
    # 3. Mostrar a ruta calculada e o seu custo por pantalla (ou informar se non existe camiño).
    # 4. Devolver o grafo orixinal.
    if graph is None:
        print("NO GRAPH FOUND")
        return graph

    origin = graph.find_by_name(origin_name)
    target = graph.find_by_name(target_name)
    for name, node in ((origin_name, origin), (target_name, target)):
        if node is None:
            print(f"NODE {name} NOT PRESENT IN GRAPH")
            return graph

    route, cost = graph.path(origin, target)
    if not route:
        print(f"NO PATH FOUND BETWEEN {origin.name} AND {target.name}")
    else:
        names = ", ".join(node.name for node in route)
        print(f"OPTIMAL PATH FROM {origin.name} TO {target.name}: [{names}] WITH COST {cost:.2f}")
    return graph