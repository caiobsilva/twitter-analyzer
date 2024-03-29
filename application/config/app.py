from application.drivers.neo4j.client import Client
from application.drivers.twitter.api_wrapper import TwitterApiWrapper
from celery import Celery

import os, tweepy

db = Client(
  os.getenv("NEO4J_URI"),
  os.getenv("NEO4J_NAME"),
  os.getenv("NEO4J_PASS")
)

# redis://:password@hostname:port/db_number
celery = Celery(
  "application",
  broker=f"redis://:{os.getenv('REDIS_PASS')}@{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0",
  include=["application.use_cases.tasks.tasks"]
)

tweepy_client = tweepy.Client(
  bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
  wait_on_rate_limit=True
)
twitter_client = TwitterApiWrapper(tweepy_client)
