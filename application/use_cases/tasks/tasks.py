from application.config.app import db, twitter_client, celery
from application.entities.missing_tweet import MissingTweet
from application.use_cases.search_tweets import SearchTweets
from application.use_cases.analyze_graph import AnalyzeGraph
from application.use_cases.repositories.user_repository import UserRepository
from neo4j import exceptions

import logging, requests, os, math

@celery.task
def query_tweets(query, start_time, amount=100000, batch_size=300, cursor_id = None):
  cursor_id = None
  repetitions = math.ceil(amount / batch_size)

  for _ in range(repetitions):
    try:
      logging.warning(f" ========= cursor: {cursor_id}")

      tweets, cursor_id = SearchTweets(twitter_client) \
        .by_stream(query, batch_size, start_time, cursor_id=cursor_id)

      UserRepository(db).create(tweets)
    except exceptions.IncompleteCommit or exceptions.ServiceUnavailable:
      query_tweets.retry(
        (query, start_time, amount, batch_size, cursor_id),
        countdown=60, max_retries=5
      )
      # query_tweets.apply_async((query, start_time, amount, batch_size, cursor_id))
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
