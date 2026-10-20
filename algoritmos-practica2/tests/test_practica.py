"""Tests da práctica de grafos.

Executar dende a carpeta `algoritmos-practica2`:
    python -m unittest discover -s tests -v
"""

import contextlib
import io
import json
import itertools
import math
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# O código da práctica impórtase como `graphs`, `commands` e `utils` dende src/graphs
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "graphs"
DATA = ROOT / "data.json"
sys.path.insert(0, str(SRC))

import commands  # noqa: E402
from graphs import Graph, Node, Order  # noqa: E402
from utils import load_json_file  # noqa: E402


def make_node(name: str, x: float = 0, y: float = 0, z: float = 0, power: float = 100) -> Node:
    """Crea un satélite de proba cos campos mínimos."""
    return Node(name, "Test", "LEO", 2000, x, y, z, power, "Active", "")


def run_command(func, *args):
    """Executa un comando e devolve (grafo resultante, texto impreso)."""
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        graph = func(*args)
    return graph, output.getvalue().strip()


def undirected(edges: str) -> Graph:
    """Constrúe un grafo non dirixido a partir dun texto tipo 'A-B B-C' (peso 1)."""
    pairs = [edge.split("-") for edge in edges.split()]
    vertices = {v for pair in pairs for v in pair}
    return Graph(vertices, {(a, b, 1) for a, b in pairs}, directed=False)


# ---------------------------------------------------------------------------
# Primeira parte: Node
# ---------------------------------------------------------------------------
class TestNode(unittest.TestCase):
    def test_distance(self):
        # Triángulo 3-4-5 nunha dimensión extra: sqrt(3² + 4² + 12²) = 13
        self.assertEqual(make_node("A").distance(make_node("B", 3, 4, 12)), 13)

    def test_equal_by_name_and_with_str(self):
        self.assertEqual(make_node("ISS"), make_node("ISS", 1, 2, 3))
        self.assertEqual(make_node("ISS"), "ISS")
        self.assertNotEqual(make_node("ISS"), make_node("Hubble"))

    def test_alphabetical_order(self):
        nodes = [make_node("C"), make_node("A"), make_node("B")]
        self.assertEqual([n.name for n in sorted(nodes)], ["A", "B", "C"])

    def test_hash_by_name(self):
        self.assertEqual(len({make_node("ISS"), make_node("ISS", 5, 5, 5)}), 1)

    def test_load_json(self):
        nodes = load_json_file(DATA)
        self.assertEqual(len(nodes), 12)
        self.assertTrue(all(isinstance(n, Node) for n in nodes))


# ---------------------------------------------------------------------------
# Segunda parte: algoritmos de Graph
# ---------------------------------------------------------------------------
class TestTravel(unittest.TestCase):
    def setUp(self):
        #     1
        #    / \
        #   4   5
        #   |   |
        #   9 - 7
        self.graph = undirected("1-4 1-5 5-7 7-9 4-9")

    def test_bfs(self):
        self.assertEqual(self.graph.travel("1", Order.WIDTH), ["1", "4", "5", "9", "7"])

    def test_bfs_is_default(self):
        self.assertEqual(self.graph.travel("1"), self.graph.travel("1", Order.WIDTH))

    def test_dfs(self):
        self.assertEqual(self.graph.travel("1", Order.DEPTH), ["1", "4", "9", "7", "5"])

    def test_only_reachable_nodes(self):
        graph = undirected("A-B C-D")
        self.assertEqual(graph.travel("A"), ["A", "B"])
        self.assertEqual(graph.travel("A", Order.DEPTH), ["A", "B"])

    def test_directed_follows_arrows(self):
        graph = Graph({"A", "B", "C"}, {("A", "B", 1), ("C", "A", 1)}, directed=True)
        self.assertEqual(graph.travel("A"), ["A", "B"])

    def test_missing_node(self):
        with self.assertRaises(ValueError):
            self.graph.travel("X")


class TestComponents(unittest.TestCase):
    def test_undirected(self):
        graph = undirected("A-B B-C D-E")
        graph.add("F")
        self.assertEqual(
            graph.connected_components(),
            {frozenset("ABC"), frozenset("DE"), frozenset("F")},
        )
        self.assertFalse(graph.is_connected())

    def test_connected(self):
        self.assertTrue(undirected("A-B B-C").is_connected())

    def test_directed_strongly_connected(self):
        # E <-> H, E -> C -> D -> F  (só E e H poden ir e volver)
        graph = Graph(
            {"C", "D", "E", "F", "H"},
            {("C", "D", 1), ("D", "F", 1), ("E", "H", 1), ("H", "E", 1), ("E", "C", 1)},
            directed=True,
        )
        self.assertEqual(
            graph.connected_components(),
            {frozenset("EH"), frozenset("C"), frozenset("D"), frozenset("F")},
        )
        self.assertFalse(graph.is_connected())

    def test_directed_cycle_is_connected(self):
        graph = Graph({"A", "B", "C"}, {("A", "B", 1), ("B", "C", 1), ("C", "A", 1)}, directed=True)
        self.assertTrue(graph.is_connected())


class TestCutVertices(unittest.TestCase):
    def test_line(self):
        self.assertEqual(undirected("A-B B-C C-D").find_cut_vertices(), {"B", "C"})

    def test_cycle_has_none(self):
        self.assertEqual(undirected("A-B B-C C-A").find_cut_vertices(), set())

    def test_root_with_two_children(self):
        # A está no medio: se se quita, B e C quedan separados
        self.assertEqual(undirected("A-B A-C").find_cut_vertices(), {"A"})

    def test_two_triangles_joined(self):
        # Dous triángulos unidos polo nodo C
        self.assertEqual(undirected("A-B B-C C-A C-D D-E E-C").find_cut_vertices(), {"C"})

    def test_several_components(self):
        self.assertEqual(undirected("A-B B-C X-Y Y-Z").find_cut_vertices(), {"B", "Y"})

    def test_directed_raises(self):
        with self.assertRaises(RuntimeError):
            Graph({"A", "B"}, {("A", "B", 1)}, directed=True).find_cut_vertices()

    def test_random_against_brute_force(self):
        # Un vértice é de corte se ao quitalo aumenta o número de compoñentes
        rng = random.Random(1)
        for _ in range(200):
            vertices = set(range(rng.randint(1, 9)))
            edges = {(a, b, 1) for a, b in itertools.combinations(vertices, 2) if rng.random() < 0.35}
            graph = Graph(vertices, edges, directed=False)
            total = len(graph.connected_components())
            expected = {
                v for v in vertices
                if len(graph.subgraph(vertices - {v}).connected_components()) > total
            }
            self.assertEqual(graph.find_cut_vertices(), expected, f"Erro con arestas {edges}")


class TestPath(unittest.TestCase):
    def test_takes_shorter_indirect_route(self):
        # Directo A-C custa 10, pero A-B-C custa 5 + 2 = 7
        graph = Graph({"A", "B", "C"}, {("A", "B", 5), ("B", "C", 2), ("A", "C", 10)}, directed=False)
        self.assertEqual(graph.path("A", "C"), (["A", "B", "C"], 7))

    def test_same_node(self):
        self.assertEqual(undirected("A-B").path("A", "A"), (["A"], 0))

    def test_no_path(self):
        self.assertEqual(undirected("A-B C-D").path("A", "D"), ([], math.inf))

    def test_directed_one_way(self):
        graph = Graph({"A", "B"}, {("A", "B", 3)}, directed=True)
        self.assertEqual(graph.path("A", "B"), (["A", "B"], 3))
        self.assertEqual(graph.path("B", "A"), ([], math.inf))

    def test_missing_node(self):
        with self.assertRaises(ValueError):
            undirected("A-B").path("A", "X")

    def test_random_against_floyd(self):
        # Compara Dijkstra coas distancias mínimas de Floyd-Warshall
        rng = random.Random(2)
        for _ in range(100):
            vertices = set(range(rng.randint(1, 8)))
            edges = {
                (a, b, rng.randint(1, 9))
                for a, b in itertools.permutations(vertices, 2) if rng.random() < 0.3
            }
            graph = Graph(vertices, edges, directed=True)
            dist = {(a, b): 0 if a == b else graph.weight(a, b) for a in vertices for b in vertices}
            for k, i, j in itertools.product(vertices, repeat=3):
                dist[i, j] = min(dist[i, j], dist[i, k] + dist[k, j])
            for a, b in itertools.product(vertices, repeat=2):
                route, cost = graph.path(a, b)
                self.assertEqual(cost, dist[a, b])
                if route:
                    self.assertEqual((route[0], route[-1]), (a, b))
                    self.assertEqual(sum(graph.weight(x, y) for x, y in zip(route, route[1:])), cost)


# ---------------------------------------------------------------------------
# Terceira parte: comandos do intérprete
# ---------------------------------------------------------------------------
class TestCommands(unittest.TestCase):
    def setUp(self):
        self.graph, self.load_output = run_command(commands.load, None, str(DATA), "40000")

    def test_load_without_connections(self):
        _, output = run_command(commands.load, None, str(DATA))
        self.assertEqual(output, "GRAPH CREATED WITH 12 NODES AND 0 EDGES")

    def test_load_range(self):
        self.assertEqual(self.load_output, "GRAPH CREATED WITH 12 NODES AND 29 EDGES")
        iss, hubble = self.graph.find_by_name("ISS"), self.graph.find_by_name("Hubble")
        # Non dirixido: a conexión existe nos dous sentidos e o peso é a distancia
        self.assertTrue(self.graph.adjacent(iss, hubble) and self.graph.adjacent(hubble, iss))
        self.assertAlmostEqual(self.graph.weight(iss, hubble), iss.distance(hubble))

    def test_load_power_is_directed(self):
        graph, output = run_command(commands.load, None, str(DATA), "--power", "800")
        self.assertEqual(output, "GRAPH CREATED WITH 12 NODES AND 24 EDGES")
        iss, hubble = graph.find_by_name("ISS"), graph.find_by_name("Hubble")
        # ISS (2500 W) alcanza 40000 km; Hubble (200 W) só ~11314 km
        self.assertTrue(graph.adjacent(iss, hubble))
        for source, target, weight in graph.edges:
            self.assertLessEqual(weight, 800 * math.sqrt(source.transmitter_power_w))

    def test_load_into_existing_graph(self):
        _, output = run_command(commands.load, self.graph, str(DATA), "40000")
        self.assertEqual(output, "INSERTED 0 NEW NODES AND 0 NEW EDGES IN GRAPH")

    def test_load_in_two_steps_equals_one_step(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = DATA.read_text(encoding="utf-8")
            nodes = json.loads(text)
            first = Path(tmp) / "first.json"
            first.write_text(json.dumps(nodes[:4]), encoding="utf-8")
            graph, out1 = run_command(commands.load, None, str(first), "15000")
            graph, out2 = run_command(commands.load, graph, str(DATA), "15000")
        self.assertEqual(out1, "GRAPH CREATED WITH 4 NODES AND 1 EDGES")
        self.assertEqual(out2, "INSERTED 8 NEW NODES AND 9 NEW EDGES IN GRAPH")
        _, full = run_command(commands.load, None, str(DATA), "15000")
        self.assertEqual(full, "GRAPH CREATED WITH 12 NODES AND 10 EDGES")

    def test_print(self):
        _, output = run_command(commands.print, self.graph)
        self.assertTrue(output.startswith("GRAPH CONTENT:"))
        self.assertIn("ISS (LEO)", output)

    def test_travel(self):
        _, output = run_command(commands.travel, self.graph, "ISS", "WIDTH")
        self.assertEqual(
            output,
            "TRAVEL WIDTH FROM ISS: [ISS, GPS-III-01, Galileo-FOC-FM1, Hubble, "
            "Meteosat-11, Sentinel-2A, Starlink-1007, Tiangong, Hispasat-30W-6]",
        )
        _, output = run_command(commands.travel, self.graph, "ISS", "DEPTH")
        self.assertTrue(output.startswith("TRAVEL DEPTH FROM ISS: [ISS, GPS-III-01, Hubble,"))

    def test_travel_missing_node(self):
        _, output = run_command(commands.travel, self.graph, "Pluto", "WIDTH")
        self.assertEqual(output, "NODE Pluto NOT PRESENT IN GRAPH")

    def test_components(self):
        _, output = run_command(commands.components, self.graph)
        self.assertEqual(
            output,
            "CONNECTED COMPONENTS: [{GPS-III-01, Galileo-FOC-FM1, Hispasat-30W-6, Hubble, ISS, "
            "Meteosat-11, Sentinel-2A, Starlink-1007, Tiangong}, {James Webb}, "
            "{Perseverance-Orbiter-Relay}, {Voyager 1}]",
        )

    def test_components_empty_graph(self):
        _, output = run_command(commands.components, Graph(directed=False))
        self.assertEqual(output, "GRAPH IS EMPTY")

    def test_cut_vertices(self):
        graph, _ = run_command(commands.load, None, str(DATA), "7100")
        _, output = run_command(commands.find_cut_vertices, graph)
        self.assertEqual(output, "CUT VERTICES: [Hubble]")

    def test_path(self):
        _, output = run_command(commands.path, self.graph, "ISS", "Meteosat-11")
        self.assertEqual(output, "OPTIMAL PATH FROM ISS TO Meteosat-11: [ISS, Meteosat-11] WITH COST 38304.90")

    def test_no_path(self):
        _, output = run_command(commands.path, self.graph, "ISS", "Voyager 1")
        self.assertEqual(output, "NO PATH FOUND BETWEEN ISS AND Voyager 1")

    def test_path_missing_node(self):
        _, output = run_command(commands.path, self.graph, "ISS", "Pluto")
        self.assertEqual(output, "NODE Pluto NOT PRESENT IN GRAPH")

    def test_no_graph(self):
        for func, args in [
            (commands.print, ()),
            (commands.travel, ("ISS",)),
            (commands.path, ("ISS", "Hubble")),
            (commands.components, ()),
            (commands.find_cut_vertices, ()),
        ]:
            _, output = run_command(func, None, *args)
            self.assertEqual(output, "NO GRAPH FOUND", func.__name__)


class TestInterpreter(unittest.TestCase):
    """Executa o intérprete real cun ficheiro de comandos, como se fai na corrección."""

    def test_full_script(self):
        script = f"""
# Comentario: debe ignorarse
LOAD "{DATA}" 40000
TRAVEL ISS WIDTH
PATH ISS "Voyager 1"
FIND_CUT_VERTICES
"""
        with tempfile.TemporaryDirectory() as tmp:
            script_file = Path(tmp) / "comandos.txt"
            script_file.write_text(script, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-B", "interpreter.py", str(script_file)],
                cwd=SRC, capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                "GRAPH CREATED WITH 12 NODES AND 29 EDGES",
                "TRAVEL WIDTH FROM ISS: [ISS, GPS-III-01, Galileo-FOC-FM1, Hubble, "
                "Meteosat-11, Sentinel-2A, Starlink-1007, Tiangong, Hispasat-30W-6]",
                "NO PATH FOUND BETWEEN ISS AND Voyager 1",
                "CUT VERTICES: []",
            ],
        )


if __name__ == "__main__":
    unittest.main()
