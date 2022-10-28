from crawler.drivers.twitter.exceptions import AuthorizationError
from typing import Any, Callable, List, Tuple

import logging, tweepy, time

class TwitterApiWrapper:
  def __init__(self, client: tweepy.Client) -> None:
    self.client = client

  def search_recent_tweets(self, **kwargs) -> Tuple[Any, dict, dict, int]:
    try:
      tweets_data, mentions, users, cursor = \
        self._call(self.client.search_recent_tweets, **kwargs)
    except AuthorizationError as e:
      logging.exception(e)
      time.sleep(2)
      tweets_data, mentions, users, cursor = \
        self._call(self.client.search_recent_tweets, **kwargs)

    return tweets_data, mentions, users, cursor

    # return self._call(self.client.search_recent_tweets, **kwargs)

  def get_tweets(self, ids: List[int], **kwargs) -> Tuple[Any, dict, dict]:
    try:
      tweets_data, mentions, users, _ = \
        self._call(self.client.get_tweets, ids=ids, **kwargs)
    # if tweet is from a private account, it is removed from the list and the request is retried
    except AuthorizationError as e:
      ids = [id for id in ids if id != e.tweet_id]
      if len(ids) == 0: return None, {}, {}
      tweets_data, mentions, users, _ = self.get_tweets(ids=ids, **kwargs)

    return tweets_data, mentions, users

  # tweepy response:
  # Response(
  #   data: list[dict<"id", "name", ...>]
  #   includes: dict<"tweets", "users">
  #   errors: list[dict<"resource_id", "title", ...>]
  # )
  def _call(self, endpoint: Callable, **kwargs) -> Tuple[Any, dict, dict, int]:
    results = endpoint(**kwargs)

    # tweepy doesn't handle API errors. this checks for tweets by private accounts
    # if len(results.errors):
    #   error = results.errors[0]
    #   if error["title"] == "Authorization Error":
    #     raise AuthorizationError(error["detail"], error["resource_id"])
    #   else:
    #     raise Exception(error["title"])

    # tweets, users and mentions (rts, quotes) come separated in different dictionaries
    tweets_data = results.data
    mentions = { m["id"]: m for m in results.includes["tweets"] }
    users = { u["id"]: u for u in results.includes["users"] }
    cursor_id = tweets_data[-1]["id"]

    return tweets_data, mentions, users, cursor_id


# TODO: includes estão vindo vazios por erro de autorização. implementar tratamento de erros e MissingTweet
# Response(
#   data=None, ,
#   includes={},
#   errors=[{'resource_id': '1581070980906045440', 'parameter': 'ids', 'resource_type': 'tweet', 'section': 'data', 'title': 'Authorization Error', 'value': '1581070980906045440', 'detail': 'Sorry, you are not authorized to see the Tweet with ids: [1581070980906045440].', 'type': 'https://api.twitter.com/2/problems/not-authorized-for-resource'}, {'resource_id': '1581070980906045440', 'parameter': 'ids', 'resource_type': 'tweet', 'section': 'data', 'title': 'Authorization Error', 'value': '1581070980906045440', 'detail': 'Sorry, you are not authorized to see the Tweet with ids: [1581070980906045440].', 'type': 'https://api.twitter.com/2/problems/not-authorized-for-resource'}, {'resource_id': '1581070980906045440', 'parameter': 'ids', 'resource_type': 'tweet', 'section': 'data', 'title': 'Authorization Error', 'value': '1581070980906045440', 'detail': 'Sorry, you are not authorized to see the Tweet with ids: [1581070980906045440].', 'type': 'https://api.twitter.com/2/problems/not-authorized-for-resource'}, {'resource_id': '1581070980906045440', 'parameter': 'ids', 'resource_type': 'tweet', 'section': 'data', 'title': 'Authorization Error', 'value': '1581070980906045440', 'detail': 'Sorry, you are not authorized to see the Tweet with ids: [1581070980906045440].', 'type': 'https://api.twitter.com/2/problems/not-authorized-for-resource'}], meta={}
# )
