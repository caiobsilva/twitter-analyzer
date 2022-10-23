import logging
from typing import List
from crawler.entities.tweet import Tweet
from crawler.drivers.neo4j.client import Client


class UserRepository:
  def __init__(self, db: Client) -> None:
    self.db = db

  def show(self, relationship: str) -> List:
    return self.db.read(f"MATCH (n)-[r:{relationship}]-(m) RETURN n, r, m")

  def create(self, tweets: List[Tweet]) -> None:
    queries = []

    for i, tweet in enumerate(tweets):
      tweet_author = tweet.author
      tweet_author_query = f"MERGE (a{i}:Author {tweet_author.as_cypher_object()})"
      parent_author_query = relationship_query = ""

      if tweet.parent is not None:
        parent_author = tweet.parent.author
        parent_author_query = f"MERGE (pa{i}:Author {parent_author.as_cypher_object()})"
        relationship_query = f"MERGE (a{i})-[:{tweet.kind}]->(pa{i})"

      queries.append(f"{parent_author_query} {tweet_author_query} {relationship_query}")

    query = " ".join(queries)
    self.db.write(query)
