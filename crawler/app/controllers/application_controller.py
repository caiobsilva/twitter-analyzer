from flask import current_app, make_response, request
from use_cases.search_tweet_data import SearchTweetData
from use_cases.tasks.tasks import get_tweets

class ApplicationController:
  def index():
    params = request.args.to_dict()

    if "query" not in params.keys():
      return make_response({ "error": "missing 'query' param" }, 400)

    search_tweet_job = current_app.config["rq"].new_queue(name="default")
    search_tweet_job.enqueue(get_tweets, params["query"])

    return make_response({}, 204)
