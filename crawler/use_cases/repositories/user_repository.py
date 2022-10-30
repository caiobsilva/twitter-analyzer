from typing import List
from crawler.entities.user import User
from crawler.entities.tweet import Tweet
from crawler.drivers.neo4j.client import Client

import logging, datetime

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

  def create2(self, tweets: List[Tweet]) -> None:
    authors = []
    relationships = []

    for i, tweet in enumerate(tweets):
      # author_obj = tweet.author
      author_obj = {
        "id": tweet.author.id,
        "name": tweet.author.name,
        "username": tweet.author.username,
        "created_at": tweet.author.created_at
      }

      if tweet.parent is not None:
        parent_author = tweet.parent.author
        # parent_obj = tweet.parent.author
        parent_obj = {
          "id": parent_author.id,
          "name": parent_author.name,
          "username": parent_author.username,
          "created_at": parent_author.created_at
        }
        relationship_obj = {
          "from": tweet.author.id,
          "to": parent_author.id,
          "kind": tweet.kind
        }

        authors.append(parent_obj)
        relationships.append(relationship_obj)

      authors.append(author_obj)

    logging.warning("#####################")
    logging.warning(authors)
    logging.warning(relationships)
    self.db.write(self._create_author_query(), authors=authors, rels=relationships)
    # user = { "id": 1, "name": "caio", "username": "caio", "created_at": datetime.datetime.now() }
    # user2 = { "id": 2, "name": "joao", "username": "joao", "created_at": datetime.datetime.now() }
    # self.db.write(self._create_author_query(), authors=[user, user2], rels=[{ "from": 1, "to": 2, "kind": "RETWEETED"}])

  def _create_author_query(self) -> str:
    query = """
      WITH $authors as authors
      UNWIND authors as author
      MERGE (a:Author {id: author.id, name: author.name, username: author.username, created_at: author.created_at})
      ON CREATE SET
        a.id = a.id,
        a.name = a.name,
        a.username = a.username,
        a.created_at = a.created_at
      ON MATCH SET
        a.name = a.name,
        a.username = a.username,
        a.created_at = a.created_at

      WITH $rels as rels
      UNWIND rels as rel
      MATCH (ra:Author) WHERE ra.id = rel.from
      MATCH (rp:Author) WHERE rp.id = rel.to
      MERGE (ra)-[r:RETWEETED]->(rp)
    """
    #MERGE (a:Author{id: author.id, name: author.name, username: author.username, created_at: author.created_at})

    # MERGE (ra:Author {id: rel.from})-[r:RETWEETED]->(rp:Author {id: rel.to})
    # ON CREATE SET
    #   ra.id = rel.from,
    #   rp.id = rel.to
    # ON MATCH SET
    #   r.kind = rel.kind
    return query

  def create3(self, tweets: List[Tweet]) -> None:
    author_queries = []
    parent_queries = []

    for i, tweet in enumerate(tweets):
      if tweet.parent is not None:
        parent_author = tweet.parent.author

        parent_queries.append({
          "id": tweet.author.id,
          "name": tweet.author.name,
          "username": tweet.author.username,
          "created_at": tweet.author.created_at ,
          "parent": {
            "id": parent_author.id,
            "name": parent_author.name,
            "username": parent_author.username,
            "created_at": parent_author.created_at
          }
        })
      else:
        author_queries.append({
          "id": tweet.author.id,
          "name": tweet.author.name,
          "username": tweet.author.username,
          "created_at": tweet.author.created_at
        })

    self.db.write(self._create_author(), authors=author_queries)
    self.db.write(self._create_author_with_parent(), authors=parent_queries)

  def _create_author(self) -> str:
    query = """
      WITH $authors as authors
      UNWIND authors as author
      MERGE (a:Author {id: author.id, name: author.name, username: author.username, created_at: author.created_at})
    """
    return query

  def _create_author_with_parent(self) -> str:
    query = """
      WITH $authors as authors
      UNWIND $authors as author
      MERGE (a:Author {id: author.id, name: author.name, username: author.username, created_at: author.created_at})
      MERGE (pa:Author {id: author.parent.id, name: author.parent.name, username: author.parent.username, created_at: author.parent.created_at})
      MERGE (a)-[:RETWEETED]->(pa)
    """
    return query
