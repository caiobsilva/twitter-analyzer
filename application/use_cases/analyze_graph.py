from typing import Any, List
import networkx as nx
import numpy as np

import statistics

class AnalyzeGraph:
  def __init__(self, nodes: Any, edges: Any) -> None:
    self.nodes = [n for n in nodes]
    self.edges = [{ "from": e.start_node["id"], "to": e.end_node["id"] } for e in edges]


  def execute(self) -> dict:
    graph = self._create_graph()
    relevant_graph = self._prune_irrelevant_nodes(graph)

    centrality = nx.pagerank(relevant_graph)
    positions = nx.spring_layout(relevant_graph, iterations=200)
    communities = self._get_node_communities(relevant_graph, centrality)

    return self._aggregate_data(relevant_graph, centrality, positions, communities)


  def _create_graph(self) -> nx.Graph:
    g = nx.Graph()

    for node in self.nodes:
      g.add_node(node._properties["id"], properties=node._properties)

    for edge in self.edges:
      g.add_edge(edge["from"], edge["to"])

    return g


  def _prune_irrelevant_nodes(self, graph: nx.Graph) -> nx.Graph:
    # remove self loop edges
    graph.remove_edges_from(nx.selfloop_edges(graph))

    # get biggest connected subgraph
    relevant_subgraph = graph.subgraph(max(nx.connected_components(graph), key=len))

    return relevant_subgraph


  def _get_node_communities(self, graph: nx.Graph, centrality_data: List) -> dict:
    # get centrality outliers
    influencer_nodes = self._get_outliers(centrality_data)

    # creates a 'supernode graph', consisting of top influencers
    supernode_graph = graph.copy()
    keep_nodes = [k for k, v in centrality_data.items() if v >= influencer_nodes[-1]]
    nodes_to_remove = [n for n in supernode_graph.nodes if n not in keep_nodes]

    for node in nodes_to_remove:
      supernode_graph.remove_node(node)

    # create weighted edges for supernode graph.
    # edge weight inversely proportional to path between nodes
    for n in supernode_graph.nodes:
      for m in supernode_graph.nodes:
        if n == m: continue
        
        path_lenght = nx.algorithms.shortest_path_length(graph, source=n, target=m)
        weight = 1 / path_lenght
        
        supernode_graph.add_weighted_edges_from([(n, m, weight)])

    # calculate communities for subgraph
    communities = nx.community.louvain_communities(supernode_graph)

    node_community_dict = {}
    for i, community in enumerate(communities):
      for node in community:
        node_community_dict[node] = i

    # add removed nodes to their closest super's community
    for node in graph:
      path_lengths = {}
      for supernode in supernode_graph:
        if node == supernode: continue

        path_lengths[supernode] = nx.algorithms.shortest_path_length(graph, source=node, target=supernode)

      influencer_supernode = min(path_lengths, key=path_lengths.get)
      if influencer_supernode is None: continue
      
      node_community_dict[node] = node_community_dict[influencer_supernode]

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


  def _get_outliers(self, centralities: dict) -> List:
    # calculate standard deviation
    threshold = 3
    centrality_data = list(centralities.values())
    mean = np.mean(centrality_data)
    std = np.std(centrality_data)
    
    outliers = []
    for y in centrality_data:
      z_score = (y - mean) / std 
      if np.abs(z_score) > threshold:
        outliers.append(y)

    # filter small outliers
    median = statistics.median(centrality_data)
    filtered_outliers = [o for o in outliers if o > median]

    return sorted(filtered_outliers, reverse=True)