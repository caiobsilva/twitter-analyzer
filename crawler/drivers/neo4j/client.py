from neo4j import GraphDatabase

class Client:
  def __init__(self, uri, user, password):
    self.driver = GraphDatabase.driver(uri, auth=(user, password))

  def create(self, tweet, retweet=None):
    with self.driver.session() as session:
      if retweet == None:
        session.write_transaction(self.create_tweet, tweet)
      else:
        session.write_transaction(self.create_retweet, tweet, retweet)
    self.driver.close()

  def create_tweet(self, tx, tweet):
    author = tweet.author

    author_query = f"MERGE (a:Author {author.as_cypher_object()})"
    tweet_query = f"MERGE (t:Tweet {tweet.as_cypher_object()})"
    relationship_query = f"MERGE (a)-[:{tweet.kind.upper()}]->(t)"

    tx.run(f"{author_query} {tweet_query} {relationship_query}")

  def create_retweet(self, tx, tweet, retweet):
    author = retweet.author
    rt_author = tweet.author

    author_query = f"MERGE (a:Author {author.as_cypher_object()})"
    rt_author_query = f"MERGE (rt_a:Author {rt_author.as_cypher_object()})"
    tweet_query = f"MERGE (t:Tweet {retweet.as_cypher_object()})"
    relationship_query = f"MERGE (a)-[:{retweet.kind.upper()}]->(t) MERGE (rt_a)-[:{tweet.kind.upper()}]->(t)"

    tx.run(f"{author_query} {tweet_query} {rt_author_query} {relationship_query}")
