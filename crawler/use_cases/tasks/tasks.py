from crawler.config.app import db, twitter_client, celery
from crawler.entities.missing_tweet import MissingTweet
from crawler.use_cases.search_tweets import SearchTweets
from crawler.use_cases.repositories.user_repository import UserRepository
import networkx as nx

import logging, requests, os, math

@celery.task
def query_tweets(query, start_time, amount=1000, batch_size=100):
  cursor_id = None
  repetitions = math.ceil(amount / batch_size)


  for _ in range(repetitions):
    try:
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
    except Exception as e:
      logging.exception(e)
      break

  analyze_graph.apply_async()

@celery.task
def analyze_graph():
  result = UserRepository(db).show()

  rels = [{ "from": rel.start_node["id"], "to": rel.end_node["id"] } for rel in result.relationships]
  nodes = [node for node in result.nodes]

  g = nx.Graph()

  for node in nodes:
    g.add_node(node.id, properties=node._properties)
    g.add_node(int(node._properties["id"]), properties=node._properties)

  for rel in rels:
    g.add_edge(rel["from"], rel["to"])

  pos = nx.spring_layout(g)

  err_count = suc_count = 0

  node_list = {}
  for node in nodes[0:1000]:
    id = node._properties["id"]
    x, y = pos[id]

    node_list[id] = node._properties

    try:
      node_list[id]["x"] = x
      node_list[id]["y"] = y

      suc_count += 1
    except Exception as e:
      logging.exception(e)
      err_count += 1

  data = { "nodes": node_list, "edges": rels }

  url = f"http://{os.getenv('APP_URI')}:5000/api/file"
  requests.post(url, json = data)
