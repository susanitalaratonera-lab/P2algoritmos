"""Módulo de utilidades: Conversión e parsing entre JSON e obxectos do tipo `Node`."""

from __future__ import annotations

import json
from pathlib import Path
import typing

from graphs.Node import Node

T = typing.TypeVar("T")


def parse_json_to_node(data: str) -> Node:
    """Parsea unha cadea JSON ao obxecto do modelo `Node`.

    Permite instanciar a entidade `Node` a partir do texto plano proporcionado
    nos comandos do intérprete[cite: 7].

    Args:
        data (str): Cadea en formato JSON cos atributos dun Node.

    Returns:
        Node: Instancia inmutable da clase `Node` inicializada cos datos.

    Raises:
        json.JSONDecodeError: Se `data` non contén un JSON sintacticamente válido.
        TypeError: Se os campos provistos non coinciden cos argumentos esperados por `Node`.
        KeyError: Se faltan campos requiridos no dicionario.
    """
    return json.loads(data, object_hook=lambda d: Node(**d))


def load_json_file(filepath: str | Path) -> list[Node] | Node:
    """Lee e deserializa un arquivo JSON nunha lista de obxectos `Node` ou unha sola instancia.
    Soporta tanto arquivos que conteñen un array JSON de nodos `[{...}, {...}]`
    como arquivos cun único obxecto `{...}`.

    Args:
        filepath (str | Path): Ruta ao arquivo JSON no sistema.

    Returns:
        list[Node] | Node: Instancia ou lista de instancias de `Node`.

    Raises:
        FileNotFoundError: Se o arquivo non existe na ruta dada.
        json.JSONDecodeError: Se o arquivo non contén un JSON ben formado.
    """
    path = Path(filepath)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f, object_hook=lambda d: Node(**d))