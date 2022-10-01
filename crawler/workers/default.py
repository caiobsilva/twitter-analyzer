import os

from drivers.rq.rq import RQ
from config.setup import Config

app = Config()

rq = RQ(
  os.getenv("REDIS_HOST"),
  os.getenv("REDIS_PORT"),
  os.getenv("REDIS_PASS")
)

listen = ["default"]

worker = rq.new_worker(listen, "default")
worker.work()
