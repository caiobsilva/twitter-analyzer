from crawler.entities.tweet import Tweet
from crawler.entities.user import User
import html

class CreateTweet:
  def __init__(self, tweet, author, parent=None, parent_author=None):
    self.tweet_obj = tweet
    self.author_obj = author
    self.parent_obj = parent
    self.parent_author_obj = parent_author

  def execute(self) -> Tweet:
    parent = self.__class__(self.parent_obj, self.parent_author_obj).execute() if self.parent_obj else None

    tweet_kind = self.tweet_obj.referenced_tweets[0].type if self.tweet_obj.referenced_tweets != None else None

    author = User(
      self.author_obj.id, html.escape(self.author_obj.name),
      self.author_obj.username, self.author_obj.created_at
    )

    tweet = Tweet(
      self.tweet_obj.id, author, html.escape(self.tweet_obj.text),
      self.tweet_obj.created_at, self.tweet_obj.source,
      self.tweet_obj.lang, kind=tweet_kind, parent=parent
    )

    return tweet
