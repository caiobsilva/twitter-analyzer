from pickletools import read_long1
from crawler.config.app import db, twitter_client, celery
from crawler.use_cases.search_tweet_data import SearchTweetData
from crawler.use_cases.repositories.user_repository import UserRepository
import networkx as nx

import logging

@celery.task
def query_tweets(query, start_time, amount=100, batch_size=100, tweet_results=100):
    cursor_id = None
    batch_amount = batch_size // tweet_results
    repetitions = amount // batch_amount

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

@celery.task
def analyze_graph():
  result = UserRepository(db).show()

  rels = [[rel.start_node["id"], rel.end_node["id"]] for rel in result.relationships]
  nodes = [dict(node) for node in result.nodes]

  g = nx.Graph()

  for node in nodes:
    g.add_node(node)

  for rel in rels:
    g.add_edge(rel)

  pos = nx.spring_layout(g)

  edge_x = edge_y = []
  pass
