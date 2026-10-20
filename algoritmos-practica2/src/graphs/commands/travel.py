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
    # TODO: [Práctica Alumno]
    # 1. Validar que o grafo non sexa None e que o nodo orixe exista no mesmo.
    # 2. Converter `order_type` ao valor do enum `Order` (ex: `Order[order_type.upper()]`), lanzando ValueError se non é válido.
    # 3. Executar `graph.travel(origin_node, order=order_enum)` para obter a lista de nodos visitados.
    # 4. Imprimir a secuencia de nodos visitados por pantalla e devolver o grafo.
    ...