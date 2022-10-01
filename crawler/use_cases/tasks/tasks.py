# from crawler import create_app
from use_cases.search_tweet_data import SearchTweetData
from config.setup import Config

def get_tweets(query, amount=10):
    app = Config()

    for _ in range(amount):
      tweets = SearchTweetData(app.twitter_client, query).execute()

      for tweet in tweets:
        app.db.create(tweet, tweet.parent)
