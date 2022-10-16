import logging
from crawler.entities.missing_user import MissingUser
from crawler.entities.tweet import Tweet
from crawler.entities.missing_tweet import MissingTweet
from crawler.use_cases.create_tweet import CreateTweet
from crawler.drivers.twitter.api_wrapper import TwitterApiWrapper
from typing import Any, Callable, Tuple, List

import math

class SearchTweets:
  EXPANSIONS = [
    "author_id", "referenced_tweets.id", "referenced_tweets.id.author_id"
  ]
  TWEET_FIELDS = [
    "created_at", "source", "referenced_tweets", "entities",
    "lang", "public_metrics", "reply_settings"
  ]
  USER_FIELDS = [
    "name", "username", "created_at"
  ]

  def __init__(self, client: TwitterApiWrapper, max_results: int = 100) -> None:
    self.client = client
    self.max_results = max_results

  def by_stream(self, query: str, batch_size: int, start_time: str, cursor_id: int = None) -> Tuple[List[Tweet], int]:
    """Returns a list of tweets for a given query by order of creation"""

    batch_amount = batch_size // self.max_results

    tweets = []
    for _ in range(batch_amount): # size of batches to be saved on db
      if cursor_id is not None: start_time = None

      tweets_data, mentions, users, cursor_id = self.client.search_recent_tweets(
        query = query,
        max_results = self.max_results,
        expansions = self.EXPANSIONS,
        user_fields = self.USER_FIELDS,
        tweet_fields = self.TWEET_FIELDS,
        since_id = cursor_id,
        start_time = start_time
      )

      tweets.extend(self._normalize_tweets(tweets_data, mentions, users))

    return tweets, cursor_id

  def by_ids(self, ids: List[int]) -> List[Tweet]:
    """Returns a list of tweets matching the given IDs"""

    unique_ids = list(set(ids))
    batches = math.ceil(len(unique_ids) / self.max_results)

    tweets = []
    for _ in range(batches):
      tweets_data, mentions, users = self.client.get_tweets(
        ids = ids,
        expansions = self.EXPANSIONS,
        user_fields = self.USER_FIELDS,
        tweet_fields = self.TWEET_FIELDS
      )

      tweets.extend(self._normalize_tweets(tweets_data, mentions, users))

    return tweets

  def _normalize_tweets(self, tweets_data: Any, mentions: dict, users: dict) -> List[Tweet]:
    """Converts a list of tweet, mention, and user API data into a structured entity list.

    _normalize_tweets([t], [m], [u]) -> [Tweet<t>(author: User<u>, parent: Tweet<t>)]"""

    tweets = []
    for tweet_data in tweets_data:
      parent_tweet = parent_author = None
      author_data = users[tweet_data.author_id]

      if tweet_data.referenced_tweets is not None:
        parent_id = tweet_data.referenced_tweets[0].id

        if parent_id in mentions.keys():
          parent_tweet = mentions[parent_id]
          parent_author = users[parent_tweet.author_id]
        else:
          parent_tweet = MissingTweet(parent_id)
          parent_author = MissingUser(int(f"00000{parent_id}"))

      tweet = CreateTweet(tweet_data, author_data, parent_tweet, parent_author).execute()
      tweets.append(tweet)

    return tweets
