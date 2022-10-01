# from crawler import create_app
from use_cases.search_tweet_data import SearchTweetData
from config.setup import Config

def get_tweets(query, start_time, amount=10):
    cursor_id = None
    app = Config()

    for _ in range(amount):
      tweets, cursor_id = SearchTweetData(
        app.twitter_client, query, cursor_id, start_time
      ).execute()

      for tweet in tweets:
        app.db.create(tweet, tweet.parent)
