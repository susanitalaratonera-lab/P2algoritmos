from Graph import Graph

vertices = {"1", "4", "5", "7", "9"}
edges = {("1", "4", "1"),
         ("1", "5", "1"),
         ("5", "7", "1"),
         ("7", "9", "1"),
         ("4", "9", "1")}

g1 = Graph(vertices=vertices, edges=edges, directed = False)
print(g1)