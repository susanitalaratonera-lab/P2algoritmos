from Graph import Graph

vertices = {"C", "D", "E", "F", "H"}
edges = {("C", "D", "1"),
         ("D", "F", "1"),
         ("E", "H", "1"),
         ("H", "E", "1"),
         ("E", "C", "1")}

g2 = Graph(vertices = vertices, edges = edges, directed = True)
print(g2)