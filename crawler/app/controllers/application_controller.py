from flask import current_app, make_response, request
from use_cases.search_tweet_data import SearchTweetData

class ApplicationController:
  def index():
    params = request.args.to_dict()

    if "query" not in params.keys():
      return make_response({ "error": "missing 'query' param" }, 400)

    tweets = SearchTweetData(current_app.config["twitter_client"], params["query"]).execute()

    for tweet in tweets:
      current_app.config["db"].create(tweet, tweet.parent)

    return make_response({ "created_tweets": len(tweets) }, 200)
