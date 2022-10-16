from crawler.config.app import db, twitter_client, celery
from crawler.entities.missing_tweet import MissingTweet
from crawler.use_cases.search_tweets import SearchTweets
from crawler.use_cases.repositories.user_repository import UserRepository
import networkx as nx

import logging, requests, os

@celery.task
def query_tweets(query, start_time, amount=100, batch_size=100):
  cursor_id = None
  repetitions = amount // batch_size

  for _ in range(repetitions):
    logging.warning(f" ========= cursor: {cursor_id}")

    tweets, cursor_id = SearchTweets(twitter_client) \
      .by_stream(query, batch_size, start_time, cursor_id=cursor_id)

    # try handling missing tweets later
    # missing_tweets = [tweet for tweet in tweets if isinstance(tweet.parent, MissingTweet)]
    # missing_parent_ids = [tweet.parent.id for tweet in missing_tweets]
    # logging.warning(missing_parent_ids)

    # missing_parents = SearchTweets(twitter_client).by_ids(missing_parent_ids)
    # for parent in missing_parents:
    #   logging.warning("\iteração missing_parents\n")
    #   for tweet in tweets:
    #     if tweet.parent.id == parent.id:
    #       tweet.parent = parent

    # logging.warning("\ncriando tweets no banco\n")
    UserRepository(db).create(tweets)

  analyze_graph.apply_async()

@celery.task
def analyze_graph():
  result = UserRepository(db).show()

  rels = [[rel.start_node["id"], rel.end_node["id"]] for rel in result.relationships]
  nodes = [node for node in result.nodes]

  g = nx.Graph()

  for node in nodes:
    g.add_node(node.id, properties=node._properties)
    g.add_node(int(node._properties["id"]), properties=node._properties)

  # todo: check if edges are coherent
  for rel in rels:
    g.add_edge(rel[0], rel[1])

  pos = nx.spring_layout(g)

  edges = []
  for edge in g.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edges.append([[x0, y0], [x1, y1]])

  err_count = suc_count = 0

  node_list = {}
  for node in nodes[0:1000]:
    id = node._properties["id"]
    x, y = pos[id]

    node_list[id] = node._properties

    try:
      node_list[id]["pos_x"] = x
      node_list[id]["pos_y"] = y

      suc_count += 1
    except Exception as e:
      print(f"{id} {e}")
      err_count += 1

  data = { "nodes": node_list, "edges": edges }

  url = f"http://{os.getenv('APP_URI')}:5000/api/file"
  requests.post(url, json = data)
