from typing import Any, List
import networkx as nx
import numpy as np

class AnalyzeGraph:
  def __init__(self, nodes: Any, edges: Any) -> None:
    self.nodes = [n for n in nodes]
    self.edges = [{ "from": e.start_node["id"], "to": e.end_node["id"] } for e in edges]

  def execute(self) -> dict:
    graph = self._create_graph()
    relevant_graph = self._prune_irrelevant_nodes(graph)

    deg_centrality = nx.degree_centrality(relevant_graph)
    positions = nx.spring_layout(relevant_graph, iterations=1000)
    # positions = nx.kamada_kawai_layout(relevant_graph)
    communities = self._get_node_communities(relevant_graph)

    return self._aggregate_data(relevant_graph, deg_centrality, positions, communities)


  def _create_graph(self) -> nx.Graph:
    g = nx.Graph()

    for node in self.nodes:
      g.add_node(node._properties["id"], properties=node._properties)

    for edge in self.edges:
      g.add_edge(edge["from"], edge["to"])

    return g

  def _prune_irrelevant_nodes(self, graph: nx.Graph) -> nx.Graph:
    # remove nodes that are part of subgraphs with < x connections
    # for component in list(nx.connected_components(graph)):
    #   if len(component) < 15:
    #     for node in component:
    #       graph.remove_node(node)

    # remove self loop edges
    graph.remove_edges_from(nx.selfloop_edges(graph))

    # get biggest connected subgraph
    relevant_subgraph = graph.subgraph(max(nx.connected_components(graph), key=len))

    return relevant_subgraph

  def _get_node_communities(self, graph: nx.Graph) -> dict:
    # creates a 'supernode graph', merging nodes with a single edge
    # to the connected node
    supernode_graph = graph.copy()
    supernode_graph.remove_edges_from(nx.selfloop_edges(supernode_graph))
    nodes_to_remove = [n for n in supernode_graph.nodes if len(list(supernode_graph.neighbors(n))) == 1]

    for node in nodes_to_remove:
      supernode_graph.remove_node(node)

    # calculate communities for subgraph
    communities = nx.community.louvain_communities(supernode_graph)

    node_community_dict = {}
    for i, community in enumerate(communities):
      for node in community:
        node_community_dict[node] = i

    # add removed nodes to their super's community
    for node in nodes_to_remove:
      neighbor = list(graph.neighbors(node))[0]
      node_community_dict[node] = node_community_dict[neighbor]

    return node_community_dict


  def _aggregate_data(self, relevant_graph: nx.Graph, centrality: dict, pos: dict, communities: dict) -> dict:
    relevant_node_ids = [node for node in relevant_graph.nodes]
    relevant_nodes = list((node._properties for node in self.nodes if node._properties["id"] in relevant_node_ids))

    for node in relevant_nodes:
      id = node["id"]

      x, y = pos[id]
      dc = centrality[id]
      community = communities[id]

      node["x"] = x
      node["y"] = y
      node["degree_centrality"] = dc
      node["community"] = community

    return { "nodes": relevant_nodes, "edges": self.edges }
