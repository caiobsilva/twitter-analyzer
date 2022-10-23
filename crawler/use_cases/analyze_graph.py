from typing import Any
import networkx as nx

class AnalyzeGraph:
  def __init__(self, nodes: Any, edges: Any) -> None:
    self.nodes = [n for n in nodes]
    self.edges = [{ "from": e.start_node["id"], "to": e.end_node["id"] } for e in edges]

  def execute(self) -> dict:
    graph = self._create_graph()

    deg_centrality = nx.degree_centrality(graph)
    positions = nx.spring_layout(graph)

    return self._aggregate_data(deg_centrality, positions)


  def _create_graph(self) -> nx.Graph:
    g = nx.Graph()

    for node in self.nodes:
      g.add_node(int(node._properties["id"]), properties=node._properties)

    for edge in self.edges:
      g.add_edge(edge["from"], edge["to"])

    return g

  def _aggregate_data(self, centrality: dict, pos: dict) -> dict:
    nodes = []
    for node in self.nodes:
      id = node._properties["id"]

      x, y = pos[id]
      dc = centrality[id]

      node._properties["x"] = x
      node._properties["y"] = y
      node._properties["degree_centrality"] = dc

      nodes.append(node._properties)

    return { "nodes": nodes, "edges": self.edges }
