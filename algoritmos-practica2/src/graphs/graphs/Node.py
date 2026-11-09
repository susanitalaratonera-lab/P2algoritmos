"""Módulo do modelo de dominio: Node (Satélites e Sondas Espaciais).

Define a entidade `Node` que representa un satélite, sonda ou estación espacial.
Inclúe coordenadas tridimensionais no espazo (x, y, z en km respecto ao centro da Terra),
potencia de emisión e metadatos operativos necesarios para a construción e análise
da rede espacial mediante grafos ponderados.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
import math
import typing


@dataclass(frozen=True)
@total_ordering
class Node:
    """Entidade inmutable que representa un satélite, estación ou sonda espacial.

    A combinación de `@dataclass(frozen=True)`, `__hash__` e `__eq__` permite empregar
    as instancias de `Node` directamente como vértices da estrutura `Graph`, servindo de
    claves en dicionarios (`dict`) e elementos en conxuntos (`set`).

    O uso de `@total_ordering` xunto con `__lt__` permite comparar e ordenar os nodos
    alfabeticamente polo seu nome, garantindo resultados deterministas e ordenados
    nas operacións de percorrido (BFS/DFS) e na xeración de informes do grafo.

    Attributes:
        name (str): Nome ou identificador único do satélite.
        agency (str): Axencia espacial operadora (ex: NASA, ESA, JAXA, SpaceX).
        orbit_type (str): Tipo de órbita (LEO, MEO, GEO, HEO, Lagrange L2, etc.).
        launch_year (int): Ano no que foi posto en órbita.
        x (float): Coordenada espacial X en quilómetros (km) respecto ao geocentro.
        y (float): Coordenada espacial Y en quilómetros (km) respecto ao geocentro.
        z (float): Coordenada espacial Z en quilómetros (km) respecto ao geocentro.
        transmitter_power_w (float): Potencia de emisión en vatios (W), empregada
            para calcular funcións de custo personalizadas en algoritmos de ruta óptima.
        status (str): Estado operativo actual ('Active', 'Standby', 'Retired').
        description (str): Breve resumo dos obxectivos da misión.
    """

    name: str
    agency: str
    orbit_type: str
    launch_year: int
    x: float
    y: float
    z: float
    transmitter_power_w: float
    status: str
    description: str

    def distance(self: typing.Self, other: Node) -> float:
        """Calcula a distancia euclidiana en 3D en quilómetros cara a outro satélite.

        Args:
            other (Node): Outro satélite con coordenadas x, y, z.

        Returns:
            float: Distancia en quilómetros (km) no espazo tridimensional.
        """
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def __eq__(self: typing.Self, other: object) -> bool:
        """Determina a igualdade entre este satélite e outro obxecto (Node ou str de nome).

        Args:
            other (object): Instancia de Node ou cadea de texto (`str`) co nome do satélite.

        Returns:
            bool: True se os nomes coinciden, False en caso contrario.
        """
        if isinstance(other, Node):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        return False

    def __lt__(self: typing.Self, other: Node | str) -> bool:
        """Determina a orde alfabética por nome.

        Permite ordenar listas de nodos de xeito determinista nos algoritmos do grafo.

        Args:
            other (Node | str): Instancia de Node ou nome do satélite a comparar.

        Returns:
            bool: True se o nome deste satélite é alfabeticamente menor, False en caso contrario.
        """
        if isinstance(other, Node):
            return self.name < other.name
        elif isinstance(other, str):
            return self.name < other
        return NotImplemented

    def __hash__(self: typing.Self) -> int:
        """Calcula o valor hash do nodo baseándose no seu nome.

        Requirido para que o nodo sexa 'hashable'.
        Permite usar Node como clave en dicionarios ou elemento en conxuntos dentro da estrutura do Grafo.

        Returns:
            int: Valor hash calculado a partir do nome.
        """
        return hash(self.name)

    def __str__(self: typing.Self) -> str:
        """Devolve unha representación lexible en texto do satélite.

        Returns:
            str: Formato 'Nome (Tipo de Órbita)'.
        """
        return f"{self.name} ({self.orbit_type})"