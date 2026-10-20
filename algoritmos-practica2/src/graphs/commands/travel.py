"""Comando do intérprete para executar percorridos BFS ou DFS no grafo."""

from __future__ import annotations

import typing

from graphs import Graph, Order


def travel(
    graph: Graph | None,
    origin_name: str,
    order_type: str = "WIDTH",
) -> Graph:
    """Executa un percorrido no grafo dende un nodo orixe indicado.

    Comportamento:
        - Selecciona o tipo de percorrido segundo o parámetro:
            * 'WIDTH': Percorrido en anchura (BFS).
            * 'DEPTH': Percorrido en profundidade (DFS).
        - Imprime a secuencia de nodos visitados durante a exploración.

    Sintaxe no script:
        TRAVEL ISS
        TRAVEL ISS WIDTH
        TRAVEL ISS DEPTH

    Args:
        graph (Graph | None): Grafo actual en memoria.
        origin_name (str): Nome do nodo orixe do percorrido.
        order_type (str): 'WIDTH' para anchura (BFS) ou 'DEPTH' para profundidade (DFS).

    Returns:
        Graph: O grafo orixinal sen modificacións.

    Raises:
        ValueError: Se o grafo é None, o nodo orixe non existe ou o tipo de percorrido non é válido.
    """
    if graph is None:
        print("NO GRAPH FOUND")
        return graph

    origin = graph.find_by_name(origin_name)
    if origin is None:
        print(f"NODE {origin_name} NOT PRESENT IN GRAPH")
        return graph

    try:
        order = Order[order_type.upper()]
    except KeyError:
        raise ValueError(f"Tipo de percorrido '{order_type}' non válido (usa WIDTH ou DEPTH).")

    visited = graph.travel(origin, order=order)
    names = ", ".join(node.name for node in visited)
    print(f"TRAVEL {order.name} FROM {origin.name}: [{names}]")
    return graph