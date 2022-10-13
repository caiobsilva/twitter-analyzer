from flask import make_response, request
from crawler.use_cases.tasks.tasks import query_tweets
from crawler.drivers.cache.json_cache import JSONCache

class ApplicationController:
  def show():
    res = JSONCache().load("test")

    return make_response(res, 200)

  def create():
    params = request.args.to_dict()

    if "query" not in params.keys():
      return make_response({ "error": "missing 'query' param" }, 400)

    query_tweets.apply_async((params["query"], params["start_time"]))

    return make_response({}, 202)

  def save_file():
    data = request.get_json()

    JSONCache().save(data, "test")

    return make_response({}, 200)
