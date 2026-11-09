"""Comando do intérprete para cargar datos dende un arquivo JSON no grafo."""

from __future__ import annotations

import itertools
import math
from pathlib import Path
import typing

from graphs import Graph, Node
from utils import load_json_file

T = typing.TypeVar("T")


def load(
    graph: Graph | None,
    filepath: str | Path,
    range_or_mode: str | None = None,
    val: str | None = None,
) -> Graph:
    """Carga os datos contidos nun arquivo JSON no grafo e xera opcionalmente as súas conexións.

    Comportamento:
        - Se o grafo recibido (`graph`) é `None`, instánciase un novo obxecto `Graph`:
            * Se se emprega o modo potencia (`--power`), créase un grafo dirixido (`directed=True`).
            * En caso contrario, créase un grafo non dirixido (`directed=False`).
        - Se o grafo xa existe (`graph is not None`), engádense os novos nodos á estrutura existente.
        - Se se especifica un alcance máximo numérico (Opción A - Radio fixo):
            * Conéctanse simetricamente (A <-> B) aqueles nodos cuxa distancia 3D
              sexa menor ou igual ao límite indicado.
        - Se se especifica o modo potencia (`--power <factor>` - Opción B):
            * Créanse arestas dirixidas (A -> B) cando a distancia non supere o alcance
              calculado segundo a potencia de transmisión do nodo orixe: R_A = factor * sqrt{P_A}.

    Nota pedagóxica de implementación:
        O arquivo indicado en `filepath` contén rexistros en formato JSON que deben
        deserializarse en instancias do modelo `Node` (mediante `utils.load_json_file`).

    Sintaxis no script:
        LOAD data.json
        LOAD data.json 200000
        LOAD data.json --power 500

    Args:
        graph (Graph | None): Grafo actual en memoria ou None se aínda non se inicializou.
        filepath (str | Path): Ruta ao arquivo JSON que contén os nodos a cargar.
        range_or_mode (str | None): Alcance máximo (float) ou flag de modo ('--power').
        val (str | None): Valor do factor de potencia cando range_or_mode é '--power'.

    Returns:
        Graph: O grafo resultante cos novos nodos e conexións cargados.

    Raises:
        FileNotFoundError: Se o arquivo especificado non existe no sistema.
        json.JSONDecodeError: Se o contido do arquivo non é un JSON válido.
        ValueError: Se o rango ou o factor de potencia non se poden converter a float.
    """
    # 1. Cargar os nodos do arquivo JSON (pode vir un só nodo ou unha lista)
    nodes = load_json_file(filepath)
    if isinstance(nodes, Node):
        nodes = [nodes]

    power_mode = range_or_mode == "--power"
    if power_mode and val is None:
        raise ValueError("O modo '--power' necesita un factor de potencia.")

    # 2. Crear o grafo ou engadir os nodos ao existente
    is_new = graph is None
    if is_new:
        graph = Graph(directed=power_mode)
    new_nodes = 0
    for node in nodes:
        if not graph.contains(node):
            graph.add(node)
            new_nodes += 1

    # 3. Conectar os nodos segundo o modo seleccionado
    new_edges = 0
    vertices = sorted(graph.vertices)
    if power_mode:
        # Opción B: A -> B se d(A, B) <= factor * sqrt(P_A)
        factor = float(val)
        for source, target in itertools.permutations(vertices, 2):
            reach = factor * math.sqrt(source.transmitter_power_w)
            if source.distance(target) <= reach and not graph.adjacent(source, target):
                graph.connect(source, target, source.distance(target))
                new_edges += 1
    elif range_or_mode is not None:
        # Opción A: A <-> B se d(A, B) <= alcance
        limit = float(range_or_mode)
        for source, target in itertools.combinations(vertices, 2):
            if source.distance(target) <= limit and not graph.adjacent(source, target):
                graph.connect(source, target, source.distance(target))
                new_edges += 1

    # 4. Mensaxe de confirmación
    if is_new:
        print(f"GRAPH CREATED WITH {new_nodes} NODES AND {new_edges} EDGES")
    else:
        print(f"INSERTED {new_nodes} NEW NODES AND {new_edges} NEW EDGES IN GRAPH")
    return graph