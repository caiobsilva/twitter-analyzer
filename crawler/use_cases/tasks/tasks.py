from crawler.config.app import db, twitter_client, celery
from crawler.use_cases.search_tweet_data import SearchTweetData
from crawler.use_cases.repositories.create_user_repository import CreateUserRepository

import logging

@celery.task
def query_tweets(query, start_time, amount=100000, batch_size=10000, tweet_results=100):
    cursor_id = None
    batch_amount = batch_size // tweet_results
    repetitions = amount // batch_amount

    for _ in range(repetitions):
      for _ in range(batch_amount):
        logging.warning(f" ========= cursor: {cursor_id}")

        try:
          tweets, cursor_id = SearchTweetData(
            twitter_client, query, cursor_id, start_time
          ).execute()
        except Exception as e:
          logging.exception("error", exc_info=e)
          break

      CreateUserRepository(db, tweets).execute()
      logging.warning(f" batch of {batch_size} tweets written to db")
