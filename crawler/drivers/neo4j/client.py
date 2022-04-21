from neo4j import GraphDatabase

class Client:
  def __init__(self, uri, user, password):
    self.driver = GraphDatabase.driver(uri, auth=(user, password))

  def create(self, tweet, parent=None):
    with self.driver.session() as session:
      if parent is None:
        session.write_transaction(self.create_tweet, tweet)
      else:
        session.write_transaction(self.create_with_parent, tweet, parent)
    self.driver.close()

  def create_tweet(self, tx, tweet):
    author = tweet.author

    author_query = f"MERGE (a:Author {author.as_cypher_object()})"
    tweet_query = f"MERGE (t:Tweet {tweet.as_cypher_object()})"
    relationship_query = f"MERGE (a)-[:{tweet.kind.upper()}]->(t)"

    tx.run(f"{author_query} {tweet_query} {relationship_query}")

  def create_with_parent(self, tx, tweet, parent):
    parent_author = parent.author
    tweet_author = tweet.author

    parent_author_query = f"MERGE (pa:Author {parent_author.as_cypher_object()})"
    tweet_author_query = f"MERGE (a:Author {tweet_author.as_cypher_object()})"

    tweet_query = f"MERGE (t:Tweet {tweet.as_cypher_object()})"

    if tweet.kind in ["quoted", "replied_to"]:
      parent_query = f"MERGE (p:Tweet {parent.as_cypher_object()})"
      relationship_query = f"MERGE (pa)-[:{parent.kind.upper()}]->(p) MERGE (a)-[:TWEETED]->(t) MERGE (t)-[:{tweet.kind.upper()}]->(p)"
    else:
      parent_query = ""
      relationship_query = f"MERGE (pa)-[:{parent.kind.upper()}]->(t) MERGE (a)-[:{tweet.kind.upper()}]->(t)"

    tx.run(f"{parent_author_query} {parent_query} {tweet_query} {tweet_author_query} {relationship_query}")
