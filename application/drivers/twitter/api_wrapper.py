from typing import Any, Callable, List, Tuple

import logging, tweepy, time

class TwitterApiWrapper:
  def __init__(self, client: tweepy.Client) -> None:
    self.client = client

  def search_recent_tweets(self, **kwargs) -> Tuple[Any, dict, dict, int]:
    tweets_data, mentions, users, cursor = \
      self._call(self.client.search_recent_tweets, **kwargs)

    return tweets_data, mentions, users, cursor

  def get_tweets(self, ids: List[int], **kwargs) -> Tuple[Any, dict, dict]:
    tweets_data, mentions, users, _ = \
      self._call(self.client.get_tweets, ids=ids, **kwargs)

    return tweets_data, mentions, users

  # tweepy response:
  # Response(
  #   data: list[dict<"id", "name", ...>]
  #   includes: dict<"tweets", "users">
  #   errors: list[dict<"resource_id", "title", ...>]
  # )
  def _call(self, endpoint: Callable, **kwargs) -> Tuple[Any, dict, dict, int]:
    try:
      results = endpoint(**kwargs)
    except KeyError:
      # patching bug on twitter API: https://github.com/tweepy/tweepy/issues/1994
      return None, {}, {}, None

    # tweets, users and mentions (rts, quotes) come separated in different dictionaries
    tweets_data = results.data
    mentions = { m["id"]: m for m in results.includes["tweets"] }
    users = { u["id"]: u for u in results.includes["users"] }
    cursor_id = tweets_data[-1]["id"]

    return tweets_data, mentions, users, cursor_id
