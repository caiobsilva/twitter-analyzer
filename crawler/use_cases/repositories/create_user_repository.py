from typing import List
from entities.tweet import Tweet
from drivers.neo4j.client import Client


class CreateUserRepository:
  def __init__(self, db: Client, tweets: List[Tweet]) -> None:
    self.db = db
    self.tweets = tweets

  def execute(self) -> None:
    queries = []

    for i, tweet in enumerate(self.tweets):
      tweet_author = tweet.author
      tweet_author_query = f"MERGE (a{i}:Author {tweet_author.as_cypher_object()})"
      parent_author_query = relationship_query = ""

      if tweet.parent is not None:
        parent_author = tweet.parent.author
        parent_author_query = f"MERGE (pa{i}:Author {parent_author.as_cypher_object()})"
        relationship_query = f"MERGE (a{i})-[:{tweet.kind.upper()}]->(pa{i})"

      queries.append(f"{parent_author_query} {tweet_author_query} {relationship_query}")

    query = " ".join(queries)
    self.db.run(query)
