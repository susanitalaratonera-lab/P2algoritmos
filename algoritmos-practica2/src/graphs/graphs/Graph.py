"""Módulo de estruturas de datos: Graph (Grafo Xenérico Ponderado).

Define a clase `Graph` e a enumeración `Order` para a representación e
manipulación de grafos (dirixidos e non dirixidos) mediante matriz de adxacencia.
Proporciona algoritmos de percorrido (BFS, DFS), análise de conectividade
(compoñentes conexas, puntos de articulación) e cálculo de rutas óptimas (Dijkstra).
"""

from __future__ import annotations
import typing
import math
import itertools
import heapq
from enum import Enum
from collections import deque

class Order(Enum):
    """Orde de exploración para os percorridos no grafo."""
    WIDTH = 1   # Percorrido en anchura (BFS)
    DEPTH = 2   # Percorrido en profundidade (DFS)


class Graph[T, Q]:
    """
    Representación dun grafo xenérico mediante unha matriz de adxacencia.

    Atributos de tipo:
        T: Tipo dos vértices (debe ser hashable e soportar ordenación).
        Q: Tipo numérico para o peso das arestas (ex. float ou int).
    """

    def __init__(self: typing.Self, vertices: set[T] = set(), edges: set[tuple[T, T, Q]] = set(), directed: bool = True) -> None:
        """
        Inicializa un novo grafo.

        :param vertices: Conxunto inicial de vértices.
        :param edges: Conxunto inicial de arestas como tuplas (orixe, destino, peso).
        :param directed: Indica se o grafo é dirixido (True) ou non dirixido (False).
        """
        self.__directed: bool = directed
        self.__vertices: list[T] = list(vertices)
        
        # Inicializa a matriz de adxacencia con False (sen conexión)
        self.__matrix: list[list[Q | bool]] = [
            [False for _ in range(len(vertices))] for _ in range(len(vertices))
        ]
        
        # Estalece as conexións iniciais
        for source, target, weight in edges:
            self.__matrix[self.__vertices.index(source)][self.__vertices.index(target)] = weight
            if not directed:
                self.__matrix[self.__vertices.index(target)][self.__vertices.index(source)] = weight

    @property
    def vertices(self: typing.Self) -> set[T]:
        """Devolve un conxunto inmutable (frozenset) cos vértices do grafo."""
        return frozenset(self.__vertices)

    @property
    def edges(self: typing.Self) -> set[tuple[T, T, Q]]:
        """Devolve o conxunto de todas as arestas actuais do grafo en forma de tuplas (orixe, destino, peso)."""
        return {
            (source, target, self.weight(source, target))
            for source, target in itertools.product(self.__vertices, repeat=2)
            if self.adjacent(source, target)
        }

    def contains(self: typing.Self, vertex: T) -> bool:
        """Comproba se un vértice existe no grafo."""
        return vertex in self.__vertices

    def find_by_name(self, name: str) -> T | None:
        """Busca un vértice no grafo para o cal o atributo 'name' coincida co nome indicado."""
        for vertex in self.__vertices:
            if vertex == name:
                return vertex
        return None

    def add(self: typing.Self, vertex: T) -> Graph[T, Q]:
        """
        Engade un novo vértice ao grafo se non existe previamente.

        :param vertex: O vértice a engadir.
        :return: A propia instancia do grafo para permitir encadeamento.
        """
        if not self.contains(vertex):
            self.__vertices.append(vertex)
            # Engade unha nova columna a cada fila existente
            for row in self.__matrix:
                row.append(False)
            # Engade a nova fila para o novo vértice
            self.__matrix.append([False for _ in range(len(self.__vertices))])
        return self

    def remove(self: typing.Self, vertex: T) -> Graph[T, Q]:
        """
        Elimina un vértice e todas as súas arestas asociadas do grafo.

        :param vertex: O vértice a eliminar.
        :return: A propia instancia do grafo.
        """
        if self.contains(vertex):
            index = self.__vertices.index(vertex)
            del self.__vertices[index]
            # Elimina a columna correspondente en cada fila
            for row in self.__matrix:
                del row[index]
            # Elimina a fila do vértice
            del self.__matrix[index]
        return self

    def adjacent_vertices(self: typing.Self, vertex: T) -> set[T]:
        """
        Obtén o conxunto de vértices adxacentes (veciños saíntes) a un vértice dado.

        :param vertex: Vértice de orixe.
        :return: Conxunto de vértices conectados directamente.
        """
        index = self.__vertices.index(vertex)
        adjacent_set = set()
        for i in range(len(self.__matrix[index])):
            if self.__matrix[index][i] is not False:
                adjacent_set.add(self.__vertices[i])
        return adjacent_set

    def adjacent(self: typing.Self, source: T, target: T) -> bool:
        """Comproba se existe unha aresta dirixida dende 'source' ata 'target'."""
        return self.__matrix[self.__vertices.index(source)][self.__vertices.index(target)] is not False

    def weight(self: typing.Self, source: T, target: T) -> Q | float:
        """
        Devolve o peso da aresta entre dous vértices.

        :return: O peso da aresta ou math.inf se non están conectados.
        """
        if self.adjacent(source, target):
            return self.__matrix[self.__vertices.index(source)][self.__vertices.index(target)]
        return math.inf

    def connect(self: typing.Self, source: T, target: T, weight: Q) -> Graph[T, Q]:
        """
        Crea ou actualiza unha aresta entre dous vértices cun peso determinado.

        :param source: Vértice orixe.
        :param target: Vértice destino.
        :param weight: Peso da conexión.
        :return: A propia instancia do grafo.
        """
        if self.contains(source) and self.contains(target):
            self.__matrix[self.__vertices.index(source)][self.__vertices.index(target)] = weight
            if not self.__directed:
                self.__matrix[self.__vertices.index(target)][self.__vertices.index(source)] = weight
        return self

    def disconnect(self: typing.Self, source: T, target: T) -> Graph[T, Q]:
        """
        Elimina a aresta entre dous vértices se existe.

        :param source: Vértice orixe.
        :param target: Vértice destino.
        :return: A propia instancia do grafo.
        """
        if self.contains(source) and self.contains(target):
            self.__matrix[self.__vertices.index(source)][self.__vertices.index(target)] = False
            if not self.__directed:
                self.__matrix[self.__vertices.index(target)][self.__vertices.index(source)] = False
        return self

    def travel(self: typing.Self, start: T, order: Order = Order.WIDTH) -> list[T]:
        """
        Realiza un percorrido determinista do grafo dende un nodo inicial (BFS ou DFS).

        :param start: Nodo de partida.
        :param order: Order.WIDTH para BFS ou Order.DEPTH para DFS.
        :return: Lista ordenada de vértices visitados.
        :raises ValueError: Se o nodo de partida non existe no grafo.
        """
        # TODO: [Práctica Alumno]
        # 1. Validar que o nodo inicial existe no grafo (lanzar ValueError se non existe).
        # 2. Implementar o percorrido segundo o tipo solicitado:
        #    - Order.WIDTH: Búsqueda en Anchura (BFS) usando unha cola.
        #    - Order.DEPTH: Búsqueda en Profundidade (DFS) usando unha pila.
        # 3. Garantir un percorrido determinista ordenando os veciños antes de procesalos.
        # 4. Devolver a lista cos vértices na orde exacta en que foron visitados.
        ...
        
    def is_connected(self: typing.Self) -> bool:
        """Indica se o grafo forma unha única compoñente conexa."""

        # TODO: [Práctica Alumno]
        # 1. Comprobar se o grafo é conexo (ou fortemente conexo se é dirixido) 
        #    verificando o número de compoñentes conexas obtidas.
        # 2. Devolver True se o grafo forma unha única compoñente, False en caso contrario.
        ...

    def connected_components(self: typing.Self) -> set[frozenset[T]]:
        """
        Calcula as compoñentes conexas (ou fortemente conexas se o grafo é dirixido).

        :return: Conxunto de conxuntos inmutables coas distintas compoñentes conexas.
        """
        # TODO: [Práctica Alumno]
        # 1. Percorrer os vértices pendentes do grafo para calcular as súas compoñentes conexas:
        #    - Grafo non dirixido: a compoñente do nodo é o conxunto dos seus descendentes.
        #    - Grafo dirixido: a compoñente é a intersección entre descendentes e ascendentes 
        #      (pode axudar ter un método `reverse` para calcular os ascendentes no grafo trasposto).
        # 2. Devolver o conxunto coas compoñentes conexas (como conxuntos/frozensets de vértices).
        ...

    def find_cut_vertices(self: typing.Self) -> set[T]:
        """
        Identifica os vértices de corte (puntos de articulación).
        Un vértice é de corte se ao eliminalo aumenta o número de compoñentes conexas.

        :return: Conxunto de nodos críticos cuxa retirada desconecta parcialmente o grafo.
        """
        # TODO: [Práctica Alumno]
        # 1. Validar que o grafo é NON dirixido (lanzar RuntimeError se é dirixido).
        # 2. Para cada compoñente conexa do grafo:
        #    a. Illar a compoñente construíndo o seu subgrafo (pode axudar ter un método `subgraph`).
        #    b. Obter o camiño DFS e a árbore de expansión a partir dun nodo inicial (pode axudar ter un método `__spanning_tree`).
        #    c. Asignar o orde de visita ('num') e calcular a menor numeración alcanzable ('low') procesando os nodos en orde inversa á DFS.
        #    d. Identificar os puntos de articulación segundo as condicións de raíz (dous ou máis fillos directos na árbore) e de nodos internos (num[u] <= low[v]).
        # 3. Devolver o conxunto cos vértices de corte atopados.
        ...

    def path(self: typing.Self, source: T, target: T) -> tuple[list[T], float]:
        """
        Atopa o camiño máis curto e a súa distancia acumulada empregando o algoritmo de Dijkstra.

        :param source: Nodo de orixe.
        :param target: Nodo destino.
        :return: Tupla con (lista de nodos do camiño, distancia total).
                 Se non hai camiño, devolve ([], math.inf).
        """
        # TODO: [Práctica Alumno]
        # 1. Validar que os nodos 'source' e 'target' existen no grafo (lanzar ValueError se non existen).
        # 2. Aplicar o algoritmo de Dijkstra utilizando unha cola de prioridade (`heapq`) para atopar 
        #    o camiño de menor peso entre 'source' e 'target'.
        # 3. Devolver a tupla (camiño, distancia_total). Se non existe camiño, devolver ([], math.inf).
        ...

    def __str__(self: typing.Self) -> str:
        """Formatea a matriz de adxacencia para a súa impresión en consola."""
        if not self.__vertices:
            return "Grafo baleiro"
        max_len_key = max(len(str(vertex)) for vertex in self.__vertices)
        max_len_val = max(len(str(v)) for r in self.__matrix for v in r)
        max_len = max(max_len_key, max_len_val)

        result = f"{' ' * max_len} {' '.join([str(vertex).rjust(max_len) for vertex in self.__vertices])}\n"
        for i in range(len(self.__vertices)):
            result += f"{str(self.__vertices[i]).rjust(max_len)} {' '.join([str(j).rjust(max_len) for j in self.__matrix[i]])}\n"
        return result