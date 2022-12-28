from application.config.app import db, twitter_client, celery
from application.entities.graph import Graph
from application.use_cases.search_tweets import SearchTweets
from application.use_cases.analyze_graph import AnalyzeGraph
from application.use_cases.repositories.user_repository import UserRepository

import logging, requests, os, math

@celery.task
def query_tweets(query, start_time, graph_id, amount=1000, batch_size=300, cursor_id = None):
  cursor_id = None
  repetitions = math.ceil(amount / batch_size)

  analysis = Graph.get(graph_id)
  analysis.status = "analyzing"
  analysis.save()

  for _ in range(repetitions):
    logging.warning(f" ========= cursor: {cursor_id}")
    
    try:
      tweets, cursor_id = SearchTweets(twitter_client) \
        .by_stream(query, batch_size, start_time, cursor_id=cursor_id)

      UserRepository(db).create(tweets)
    except Exception as e:
      analysis.status = "error"
      analysis.save()

      logging.exception(e)
      break

  analyze_graph.apply_async((graph_id,))


@celery.task
def analyze_graph(graph_id: str):
  analysis = Graph.get(graph_id)

  analysis.status = "analyzing"
  analysis.save()

  try:
    result = UserRepository(db).show("RETWEETED")
    data = AnalyzeGraph(result.nodes, result.relationships).execute()

    analysis.status = "done"
    analysis.save()
  except:
    analysis.status = "error"
    analysis.save()

  url = f"http://{os.getenv('APP_URI')}:5000/api/file"
  requests.post(url, json = data)
