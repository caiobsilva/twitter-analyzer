import redis

from rq import Worker, Queue, Connection

class RQ:
  def __init__(self, host, port, password):
    self.conn = redis.Redis(host=host, port=port, password=password)

  def new_queue(self, name="default", timeout=3600):
    return Queue(name, connection=self.conn, default_timeout=timeout)

  def new_worker(self, queues, name):
    return Worker(queues, name=name, connection=self.conn)
