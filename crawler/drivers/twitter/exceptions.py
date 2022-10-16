class AuthorizationError(Exception):
  def __init__(self, message: str, tweet_id: int):
    self.message = message
    self.tweet_id = tweet_id

  def __str__(self):
    return self.message
