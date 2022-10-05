import os

from crawler.drivers.rq.rq import RQ
from crawler.config.app import App

app = App()

rq = RQ(
  os.getenv("REDIS_HOST"),
  os.getenv("REDIS_PORT"),
  os.getenv("REDIS_PASS")
)

listen = ["default"]

worker = rq.new_worker(listen, "default")
worker.work()
