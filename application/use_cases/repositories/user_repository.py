from typing import List
from application.entities.tweet import Tweet
from application.drivers.neo4j.client import Client

class UserRepository:
  def __init__(self, db: Client) -> None:
    self.db = db

  def show(self, relationship: str) -> List:
    return self.db.read(f"MATCH (n)-[r:{relationship}]-(m) RETURN n, r, m LIMIT 10000")

  def create(self, tweets: List[Tweet]) -> None:
    author_queries = []
    parent_queries = []

    for tweet in tweets:
      author_dict = vars(tweet.author)

      if tweet.parent is not None:
        parent_author = tweet.parent.author
        parent_dict = { "parent": vars(parent_author) }

        parent_queries.append(author_dict | parent_dict)
      else:
        author_queries.append(author_dict)

    self.db.write(self._create_author_query(), authors=author_queries)
    self.db.write(self._create_author_with_parent_query(), authors=parent_queries)

  def _create_author_query(self) -> str:
    query = """
      WITH $authors as authors
      UNWIND authors as author
      MERGE (a:Author {id: author.id, name: author.name, username: author.username, created_at: author.created_at})
    """
    return query

  def _create_author_with_parent_query(self) -> str:
    query = """
      WITH $authors as authors
      UNWIND $authors as author
      MERGE (a:Author {id: author.id, name: author.name, username: author.username, created_at: author.created_at})
      MERGE (pa:Author {id: author.parent.id, name: author.parent.name, username: author.parent.username, created_at: author.parent.created_at})
      MERGE (a)-[:RETWEETED]->(pa)
    """
    return query
