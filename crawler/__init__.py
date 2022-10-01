import os, tweepy

from flask import Flask
from drivers.neo4j.client import Client
from drivers.rq.rq import RQ
from app.config.routes import application_bp

def create_app():
  # setup flask api
  app = Flask("crawler")
  app.register_blueprint(application_bp, url_prefix="/")

  with app.app_context():
    # create neo4j instance
    db = Client(
      os.getenv("NEO4J_URI"),
      os.getenv("NEO4J_NAME"),
      os.getenv("NEO4J_PASS")
    )
    app.config["db"] = db

    # create redis instance
    rq = RQ(
      os.getenv("REDIS_HOST"),
      os.getenv("REDIS_PORT"),
      os.getenv("REDIS_PASS")
    )
    app.config["rq"] = rq

    # authenticate credentials with twitter API
    twitter_client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))
    app.config["twitter_client"] = twitter_client

  return app
