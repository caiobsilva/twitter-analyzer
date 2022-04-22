import os, tweepy

from flask import Flask
from drivers.neo4j.client import Client
from app.config.routes import application_bp

if __name__ == "__main__":
  # setup flask api
  app = Flask("crawler")
  app.register_blueprint(application_bp, url_prefix="/")

  # create neo4j instance
  db = Client(
    os.getenv("NEO4J_URI"),
    os.getenv("NEO4J_NAME"),
    os.getenv("NEO4J_PASS")
  )
  app.config["db"] = db

  # authenticate credentials with twitter API
  twitter_client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))
  app.config["twitter_client"] = twitter_client

  app.run(host="0.0.0.0", port=5000, debug=True)
