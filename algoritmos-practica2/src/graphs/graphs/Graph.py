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
        if not self.contains(start):
            raise ValueError(f"O nodo '{start}' non existe no grafo.")

        # Percorrido en profundidade (DFS): reutiliza a árbore de expansión
        if order == Order.DEPTH:
            visited, _ = self.__spanning_tree(start)
            return visited

        # Percorrido en anchura (BFS): cola FIFO
        visited: list[T] = []
        seen: set[T] = {start}       # Nodos xa engadidos á cola (para non repetilos)
        queue: deque[T] = deque([start])
        while queue:
            vertex = queue.popleft()  # Saca polo principio (o máis antigo)
            visited.append(vertex)
            # Veciños en orde alfabética para que o percorrido sexa determinista
            for neighbour in sorted(self.adjacent_vertices(vertex)):
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        return visited

    def __spanning_tree(self: typing.Self, start: T) -> tuple[list[T], dict[T, T | None]]:
        """
        Realiza un percorrido en profundidade (DFS) e constrúe a súa árbore de expansión.

        :param start: Nodo raíz do percorrido.
        :return: Tupla con (lista de nodos na orde DFS, dicionario fillo -> pai na árbore).
                 O pai da raíz é None.
        """
        visited: list[T] = []
        parent: dict[T, T | None] = {}
        # A pila garda parellas (nodo, pai dende o que se descubriu)
        stack: deque[tuple[T, T | None]] = deque([(start, None)])
        while stack:
            vertex, vertex_parent = stack.pop()  # Saca polo final (o máis recente)
            if vertex in parent:
                continue  # Xa visitado por outro camiño
            parent[vertex] = vertex_parent
            visited.append(vertex)
            # Apílanse en orde inversa para que o alfabeticamente menor saia primeiro
            for neighbour in sorted(self.adjacent_vertices(vertex), reverse=True):
                if neighbour not in parent:
                    stack.append((neighbour, vertex))
        return visited, parent

    def reverse(self: typing.Self) -> Graph[T, Q]:
        """Devolve o grafo trasposto (mesmos vértices coas arestas en sentido contrario)."""
        return Graph(
            set(self.__vertices),
            {(target, source, weight) for source, target, weight in self.edges},
            self.__directed,
        )

    def subgraph(self: typing.Self, vertices: set[T]) -> Graph[T, Q]:
        """Devolve o subgrafo formado polos vértices indicados e as arestas entre eles."""
        return Graph(
            set(vertices),
            {
                (source, target, weight)
                for source, target, weight in self.edges
                if source in vertices and target in vertices
            },
            self.__directed,
        )

    def is_connected(self: typing.Self) -> bool:
        """Indica se o grafo forma unha única compoñente conexa."""
        return len(self.connected_components()) == 1

    def connected_components(self: typing.Self) -> set[frozenset[T]]:
        """
        Calcula as compoñentes conexas (ou fortemente conexas se o grafo é dirixido).

        :return: Conxunto de conxuntos inmutables coas distintas compoñentes conexas.
        """
        components: set[frozenset[T]] = set()
        pending: set[T] = set(self.__vertices)  # Vértices aínda sen compoñente asignada
        reversed_graph = self.reverse() if self.__directed else None

        while pending:
            vertex = next(iter(pending))
            # Descendentes: nodos alcanzables dende o vértice
            component = set(self.travel(vertex))
            if reversed_graph is not None:
                # Ascendentes: nodos que alcanzan o vértice (descendentes no trasposto)
                component &= set(reversed_graph.travel(vertex))
            components.add(frozenset(component))
            pending -= component
        return components

    def find_cut_vertices(self: typing.Self) -> set[T]:
        """
        Identifica os vértices de corte (puntos de articulación).
        Un vértice é de corte se ao eliminalo aumenta o número de compoñentes conexas.

        :return: Conxunto de nodos críticos cuxa retirada desconecta parcialmente o grafo.
        """
        if self.__directed:
            raise RuntimeError("Os vértices de corte só se calculan en grafos non dirixidos.")

        cut_vertices: set[T] = set()
        for component in self.connected_components():
            # a. Illar a compoñente
            sub = self.subgraph(component)
            root = min(component)

            # b. Percorrido DFS e árbore de expansión
            order, parent = sub.__spanning_tree(root)
            children: dict[T, list[T]] = {vertex: [] for vertex in order}
            for vertex, vertex_parent in parent.items():
                if vertex_parent is not None:
                    children[vertex_parent].append(vertex)

            # c. num = orde de visita; low = menor num alcanzable baixando pola
            #    árbore e subindo como moito por unha aresta de retroceso.
            #    En orde inversa, os fillos procésanse sempre antes que o pai.
            num = {vertex: index for index, vertex in enumerate(order)}
            low: dict[T, int] = {}
            for u in reversed(order):
                low[u] = num[u]
                for w in sub.adjacent_vertices(u):
                    if parent[w] == u:
                        low[u] = min(low[u], low[w])  # Fillo na árbore
                    elif w != parent[u]:
                        low[u] = min(low[u], num[w])  # Aresta de retroceso

            # d. Raíz: é de corte se ten dous ou máis fillos na árbore
            if len(children[root]) >= 2:
                cut_vertices.add(root)
            # Nodo interno u: é de corte se algún fillo v non pode subir por riba de u
            for u in order[1:]:
                if any(num[u] <= low[v] for v in children[u]):
                    cut_vertices.add(u)
        return cut_vertices

    def path(self: typing.Self, source: T, target: T) -> tuple[list[T], float]:
        """
        Atopa o camiño máis curto e a súa distancia acumulada empregando o algoritmo de Dijkstra.

        :param source: Nodo de orixe.
        :param target: Nodo destino.
        :return: Tupla con (lista de nodos do camiño, distancia total).
                 Se non hai camiño, devolve ([], math.inf).
        """
        if not self.contains(source):
            raise ValueError(f"O nodo '{source}' non existe no grafo.")
        if not self.contains(target):
            raise ValueError(f"O nodo '{target}' non existe no grafo.")

        distances: dict[T, float] = {vertex: math.inf for vertex in self.__vertices}
        previous: dict[T, T] = {}       # Nodo anterior no mellor camiño coñecido
        distances[source] = 0
        heap: list[tuple[float, T]] = [(0, source)]  # Cola de prioridade (distancia, nodo)
        done: set[T] = set()            # Nodos con distancia xa definitiva

        while heap:
            distance, vertex = heapq.heappop(heap)  # Nodo pendente máis próximo
            if vertex in done:
                continue  # Entrada antiga da cola cunha distancia peor
            done.add(vertex)
            if vertex == target:
                break
            for neighbour in sorted(self.adjacent_vertices(vertex)):
                new_distance = distance + self.weight(vertex, neighbour)
                if new_distance < distances[neighbour]:
                    distances[neighbour] = new_distance
                    previous[neighbour] = vertex
                    heapq.heappush(heap, (new_distance, neighbour))

        if distances[target] == math.inf:
            return [], math.inf

        # Reconstrúe o camiño cara atrás dende o destino ata a orixe
        path = [target]
        while path[-1] != source:
            path.append(previous[path[-1]])
        path.reverse()
        return path, distances[target]

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