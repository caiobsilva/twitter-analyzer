from flask import make_response, request
from crawler.use_cases.tasks.tasks import query_tweets
from crawler.use_cases.repositories.user_repository import UserRepository
from crawler.config.app import db

class ApplicationController:
  def show():
    result = UserRepository(db).show()

    rels = [[rel.start_node["id"], rel.end_node["id"]] for rel in result.relationships]
    nodes = [dict(node) for node in result.nodes]

    res = { "nodes": nodes, "edges": rels }

    return make_response(res, 200)

  def create():
    params = request.args.to_dict()

    if "query" not in params.keys():
      return make_response({ "error": "missing 'query' param" }, 400)

    query_tweets.apply_async((params["query"], params["start_time"]))

    return make_response({}, 202)
