from neo4j import GraphDatabase

class Client:
  def __init__(self, uri, user, password):
    self.driver = GraphDatabase.driver(uri, auth=(user, password))

  def create(self, tweet):
    with self.driver.session() as session:
      session.write_transaction(self.create_tweet, tweet)
    self.driver.close()

  def create_tweet(self, tx, tweet):
    tx.run(
      "MERGE (a:Author {id: $author_id, name: $name, username: $username}) "
      "MERGE (t:Tweet {id: $id, author_id: $author_id, text: $text, created_at: $created_at}) "
      "MERGE (a)-[:TWEETED]->(t)",
      id = tweet.id, author_id = tweet.author.id, text = tweet.text, created_at = tweet.created_at,
      name = tweet.author.name, username = tweet.author.username
    )
