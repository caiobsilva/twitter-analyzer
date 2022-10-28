from time import sleep
from typing import Any, List
from neo4j import GraphDatabase, exceptions

import logging

class Client:
  ATTEMPTS = 15

  def __init__(self, uri: str, user: str, password: str):
    self.driver = GraphDatabase.driver(uri, auth=(user, password))

    with self.driver.session() as session:
      session.run(
        "CREATE INDEX author_attrs IF NOT EXISTS FOR (n:Author) ON (n.id, n.username, n.name, n.created_at)"
      )

  def read(self, query) -> List[Any]:
    with self.driver.session() as session:
      result = self.run(session.read_transaction, query)
    self.driver.close()
    return result

  def write(self, query) -> List[Any]:
    with self.driver.session() as session:
      # result = session.run(query).graph()
      result = self.run(session.write_transaction, query)

    self.driver.close()
    return result

  def run(self, method, query) -> List[Any]:
    for attempt in range(self.ATTEMPTS):
      # try:
      return method(self.run_query, query)

      # except exceptions.IncompleteCommit or exceptions.ServiceUnavailable:
      #   logging.warning("Service unavailable")
      #   sleep(5)
      #   if attempt >= self.ATTEMPTS: raise

  def run_query(self, tx, query):
    result = tx.run(query)
    return result.graph()
