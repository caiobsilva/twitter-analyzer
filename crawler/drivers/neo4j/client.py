from time import sleep
from neo4j import GraphDatabase, exceptions

import logging

class Client:
  ATTEMPTS = 5

  def __init__(self, uri: str, user: str, password: str):
    self.driver = GraphDatabase.driver(uri, auth=(user, password))

  def run(self, query) -> None:
    for attempt in range(self.ATTEMPTS):
      try:
        with self.driver.session() as session:
          result = lambda tx: tx.run(f"{query}")
          session.write_transaction(result)

        self.driver.close()
      except exceptions.IncompleteCommit or exceptions.ServiceUnavailable:
        logging.warning("Service unavailable")
        sleep(5)
        if attempt >= self.ATTEMPTS: raise
