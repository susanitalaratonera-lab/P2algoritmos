"""Paquete que expón o catálogo de comandos executables polo intérprete.

Cada módulo neste paquete implementa un comando concreto compatible co intérprete.
O intérprete mapea a primeira palabra de cada liña lida nun script (en minúsculas)
coa función correspondente aquí exportada.

Comandos dispoñibles na práctica de grafos:
    - LOAD <ruta_ficheiro> [alcance_máx]: Carga satélites dende un JSON e conecta opcionalmente por distancia.
    - PRINT: Imprime a estrutura do grafo (matriz de adxacencia).
    - TRAVEL <orixe> [WIDTH|DEPTH]: Executa un percorrido en anchura (BFS) ou profundidade (DFS).
    - PATH <orixe> <destino>: Calcula o camiño máis curto entre dous nodos mediante Dijkstra.
    - COMPONENTS: Identifica e amosa as compoñentes conexas da rede.
    - CUT_VERTICES: Atopa os puntos de articulación (vértices de corte) do grafo.
"""

from .components import components
from .find_cut_vertices import find_cut_vertices
from .load import load
from .path import path
from .print import print
from .travel import travel

__all__ = [
    "components",
    "find_cut_vertices",
    "load",
    "path",
    "print",
    "travel",
]
