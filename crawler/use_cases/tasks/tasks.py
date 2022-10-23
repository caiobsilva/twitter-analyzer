from crawler.config.app import db, twitter_client, celery
from crawler.entities.missing_tweet import MissingTweet
from crawler.use_cases.search_tweets import SearchTweets
from crawler.use_cases.analyze_graph import AnalyzeGraph
from crawler.use_cases.repositories.user_repository import UserRepository
import networkx as nx

import logging, requests, os, math

@celery.task
def query_tweets(query, start_time, amount=200, batch_size=100):
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
  result = UserRepository(db).show("RETWEETED")

  data = AnalyzeGraph(result.nodes, result.relationships).execute()

  url = f"http://{os.getenv('APP_URI')}:5000/api/file"
  requests.post(url, json = data)
