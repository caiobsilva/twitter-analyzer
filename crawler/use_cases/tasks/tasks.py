from config.setup import Config
from use_cases.search_tweet_data import SearchTweetData
from use_cases.repositories.create_user_repository import CreateUserRepository

import logging

def get_tweets(query, start_time, amount=1000):
    cursor_id = None
    app = Config()

    for _ in range(amount):
      logging.warning(f" ========= cursor: {cursor_id}")

      try:
        tweets, cursor_id = SearchTweetData(
          app.twitter_client, query, cursor_id, start_time
        ).execute()

        CreateUserRepository(app.db, tweets).execute()
      except TypeError as e:
        logging.exception("error", exc_info=e)
        continue
      except Exception as e:
        logging.exception("error", exc_info=e)
        break
    logging.warning(f" ========= ended {amount} loops")
