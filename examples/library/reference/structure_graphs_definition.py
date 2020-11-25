from gsurface.advanced.structure.graph import StructureGraph, InteractionParameters, Solid
from gsurface.advanced.structure.structures import CarStructure, TriangleStructure

graph = StructureGraph()
graph.nodes.extend([Solid() for i in range(4)])  # masses
graph.interactions.update({
    (0, 1): InteractionParameters(),
    (2, 3): InteractionParameters(),
    (0, 3): InteractionParameters()
})

graph[0, 1].stiffness = 10.0

print("graph", graph.isConsistant())
print(graph)
print(graph.__dict__)
print("TriangleStructure", TriangleStructure().isConsistant())
print("SquareStructure", CarStructure().isConsistant())
