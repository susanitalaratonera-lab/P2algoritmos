"""Comando do intérprete para cargar datos dende un arquivo JSON no grafo."""

from __future__ import annotations

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
    # TODO: [Práctica Alumno]
    # 1. Cargar os nodos do arquivo JSON mediante `load_json_file(filepath)`.
    # 2. Se `graph` é None, instanciar un novo `Graph` (dirixido se range_or_mode == "--power", non dirixido en caso contrario).
    #    Se xa existe, engadir os novos nodos á estrutura.
    # 3. Crear as conexións entre os nodos do grafo segundo o modo seleccionado:
    #    - Modo potencia (`--power <val>`): Conectar dirixidamente A -> B se d(A,B) <= val * sqrt(power_A).
    #    - Modo radio fixo (`<limit>`): Conectar simetricamente A <-> B se d(A,B) <= limit.
    # 4. Imprimir a mensaxe de confirmación e devolver o grafo.
    ...