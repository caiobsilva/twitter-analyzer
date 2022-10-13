from crawler.config.app import db, twitter_client, celery
from crawler.use_cases.search_tweet_data import SearchTweetData
from crawler.use_cases.repositories.user_repository import UserRepository
import networkx as nx

import logging, requests, os

@celery.task
def query_tweets(query, start_time, amount=100, batch_size=100, tweet_results=100):
    cursor_id = None
    batch_amount = batch_size // tweet_results
    repetitions = amount // batch_size

    for _ in range(repetitions):
      for _ in range(batch_amount):
        logging.warning(f" ========= cursor: {cursor_id}")

        try:
          tweets, cursor_id = SearchTweetData(
            twitter_client, query, cursor_id, start_time
          ).execute()
        except Exception as e:
          logging.exception("error", exc_info=e)
          break

      UserRepository(db).create(tweets)
      logging.warning(f" batch of {batch_size} tweets written to db")

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
