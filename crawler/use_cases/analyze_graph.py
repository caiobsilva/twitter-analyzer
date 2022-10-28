import logging
from typing import Any, List
import networkx as nx

class AnalyzeGraph:
  def __init__(self, nodes: Any, edges: Any) -> None:
    self.nodes = [n for n in nodes]
    self.edges = [{ "from": e.start_node["id"], "to": e.end_node["id"] } for e in edges]

  def execute(self) -> dict:
    graph = self._create_graph()
    relevant_graph = self._prune_irrelevant_nodes(graph)

    deg_centrality = nx.degree_centrality(relevant_graph)
    positions = nx.spring_layout(relevant_graph)
    # positions = nx.kamada_kawai_layout(relevant_graph)

    return self._aggregate_data(relevant_graph, deg_centrality, positions)


  def _create_graph(self) -> nx.Graph:
    g = nx.Graph()

    for node in self.nodes:
      g.add_node(int(node._properties["id"]), properties=node._properties)

    for edge in self.edges:
      g.add_edge(edge["from"], edge["to"])

    return g

  def _prune_irrelevant_nodes(self, graph: nx.Graph) -> nx.Graph:
    # remove nodes that are part of subgraphs with < 4 connections
    for component in list(nx.connected_components(graph)):
      if len(component) < 4:
        for node in component:
          graph.remove_node(node)

    return graph

  def _aggregate_data(self, relevant_graph: nx.Graph, centrality: dict, pos: dict) -> dict:
    relevant_node_ids = [node for node in relevant_graph.nodes]
    relevant_nodes = list((node._properties for node in self.nodes if node._properties["id"] in relevant_node_ids))

    for node in relevant_nodes:
      id = node["id"]

      x, y = pos[id]
      dc = centrality[id]

      node["x"] = x
      node["y"] = y
      node["degree_centrality"] = dc

    return { "nodes": relevant_nodes, "edges": self.edges }
