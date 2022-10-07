from flask import make_response, request
from crawler.use_cases.tasks.tasks import query_tweets

class ApplicationController:
  def index():
    params = request.args.to_dict()

    if "query" not in params.keys():
      return make_response({ "error": "missing 'query' param" }, 400)

    query_tweets.apply_async((params["query"], params["start_time"]))

    return make_response({}, 202)
