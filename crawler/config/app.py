from crawler.drivers.neo4j.client import Client
from crawler.drivers.twitter.api_wrapper import TwitterApiWrapper
from celery import Celery

import os, tweepy

db = Client(
  os.getenv("NEO4J_URI"),
  os.getenv("NEO4J_NAME"),
  os.getenv("NEO4J_PASS")
)

# redis://:password@hostname:port/db_number
celery = Celery(
  "crawler",
  broker=f"redis://:{os.getenv('REDIS_PASS')}@{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0",
  include=["crawler.use_cases.tasks.tasks"]
)

tweepy_client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))
twitter_client = TwitterApiWrapper(tweepy_client)
