from flask import make_response, request
from application.use_cases.tasks.tasks import query_tweets, analyze_graph
from application.use_cases.search_tweets import SearchTweets
from application.drivers.cache.json_cache import JSONCache
from application.config.app import twitter_client

class ApplicationController:
  def show():
    res = JSONCache().load("test")

    response = make_response(res, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

  def create():
    params = request.args.to_dict()

    if "query" not in params.keys():
      return make_response({ "error": "missing 'query' param" }, 400)

    query_tweets.apply_async(
      (params["query"], params["start_time"]),
      { "cursor_id": params["cursor_id"] }
    )

    return make_response({}, 202)

  # debug
  def find_by_id():
    params = request.args.to_dict()

    if "id" not in params.keys():
      return make_response({ "error": "missing 'id' param" }, 400)

    tweets = SearchTweets(twitter_client).by_ids([params["id"]])

    return make_response({ "tweets": [tweet.id for tweet in tweets] }, 200)

  # debug
  def save_file():
    data = request.get_json()

    JSONCache().save(data, "test")

    return make_response({}, 200)

  # debug
  def analyze():
    analyze_graph.apply_async()

    return make_response({}, 202)
