from time import sleep
from typing import Any, List
from neo4j import GraphDatabase, exceptions

import logging

class Client:
  ATTEMPTS = 15

  def __init__(self, uri: str, user: str, password: str):
    self.driver = GraphDatabase.driver(uri, auth=(user, password))

    with self.driver.session() as session:
      session.run("CREATE INDEX author_attrs IF NOT EXISTS FOR (n:Author) ON (n.id)")

  def read(self, query) -> List[Any]:
    with self.driver.session() as session:
      result = self.run(session.read_transaction, query)

    self.driver.close()
    return result

  def write(self, query, **kwargs) -> List[Any]:
    with self.driver.session() as session:
      result = self.run(session.write_transaction, query, **kwargs)

    self.driver.close()
    return result

  def run(self, method, query, **kwargs) -> List[Any]:
    return method(self.run_query, query, **kwargs)

  def run_query(self, tx, query, **kwargs):
    result = tx.run(query, **kwargs)
    return result.graph()
