import os, tweepy

from drivers.neo4j.client import Client
from drivers.rq.rq import RQ

class Config:
  def __init__(self):
    self.db = Client(
      os.getenv("NEO4J_URI"),
      os.getenv("NEO4J_NAME"),
      os.getenv("NEO4J_PASS")
    )

    # create redis instance
    self.rq = RQ(
      os.getenv("REDIS_HOST"),
      os.getenv("REDIS_PORT"),
      os.getenv("REDIS_PASS")
    )

    # authenticate credentials with twitter API
    self.twitter_client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))
