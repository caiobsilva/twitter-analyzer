from entities.tweet import Tweet
from use_cases.create_tweet import CreateTweet
from typing import List
import tweepy

class SearchTweetData:
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

  def __init__(self, client: tweepy.Client, query: str, max_results: int = 100):
    self.client = client
    self.query = query
    self.max_results = max_results

  def execute(self):
    results = self.client.search_recent_tweets(
      query = self.query,
      max_results = self.max_results,
      expansions = self.EXPANSIONS,
      user_fields = self.USER_FIELDS,
      tweet_fields = self.TWEET_FIELDS
    )

    # tweets, users and mentions (rts, quotes) come separated in different dictionaries
    tweets_data = results.data
    mentions = { m["id"]: m for m in results.includes["tweets"] }
    users = { u["id"]: u for u in results.includes["users"] }

    tweets = []
    for tweet_data in tweets_data:
      author_data = users[tweet_data.author_id]

      if tweet_data.referenced_tweets is not None:
        parent_id = tweet_data.referenced_tweets[0].id

        parent_tweet = mentions[parent_id]
        parent_author = users[parent_tweet.author_id]

        tweet = CreateTweet(tweet_data, author_data, parent_tweet, parent_author).execute()
      else:
        tweet = CreateTweet(tweet_data, author_data).execute()

      tweets.append(tweet)

    return tweets
