from flask import make_response, request, jsonify
from application.use_cases.tasks.tasks import query_tweets, analyze_graph
from application.drivers.cache.json_cache import JSONCache
from application.entities.graph import Graph
from application.config.app import celery
from datetime import datetime

class ApplicationController:
  def show():
    res = JSONCache().load("test")

    response = make_response(res, 200)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


  def create():
    params = request.args.to_dict()

    if not all(param in ["query", "start_time"] for param in params):
      response = make_response({ "error": "missing params" }, 400)
    else:
      start_time = datetime.strptime(params["start_time"], "%Y-%m-%d")
      query_tweets.apply_async((params["query"], start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")))
      
      graph_data = Graph.create(params["query"])
      response = make_response(vars(graph_data), 202)

    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


  def analyses():
    analyses = JSONCache().load_all()

    response = jsonify(analyses)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


  # debug
  def analyze():
    analyze_graph.apply_async()

    return make_response({}, 202)


  # this is a workaround as I'm not willing to implement another 
  # database for this project. for a production tool, a database
  # such as S3 should be used
  def save_file():
    data = request.get_json()

    JSONCache().save(data, data["id"])

    return make_response({}, 200)
