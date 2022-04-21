import tweepy, configparser
from drivers.neo4j.client import Client
from use_cases.create_tweet import CreateTweet

# read authentication credentials
config = configparser.RawConfigParser()
config.read(".env")

# create neo4j instance
neo4j_creds = config["neo4j"]
neo4j = Client(neo4j_creds["neo4j_uri"], neo4j_creds["neo4j_name"], neo4j_creds["neo4j_pass"])

# authenticate credentials with twitter API
bearer_token = config["twitter"]["bearer_token"]
client = tweepy.Client(bearer_token=bearer_token)

# get tweets
tweets = client.search_recent_tweets(
  query="bolsonaro",
  tweet_fields=["created_at", "source", "referenced_tweets", "entities", "lang", "public_metrics", "reply_settings"],
  user_fields=["name", "username", "created_at"],
  max_results=10,
  expansions=["author_id", "referenced_tweets.id", "referenced_tweets.id.author_id"]
)

# create users and retweets dictionary
users = { u["id"]: u for u in tweets.includes["users"] }
retweets = { rt["id"]: rt for rt in tweets.includes["tweets"] }

for tweet_data in tweets.data:
  # get related data (parent tweets, users)
  author_data = users[tweet_data.author_id] if users[tweet_data.author_id] else None
  parent_id = tweet_data.referenced_tweets[0].id if tweet_data.referenced_tweets != None else None
  parent_tweet = retweets[parent_id] if parent_id else None
  parent_author = users[parent_tweet.author_id] if parent_tweet else None

  tweet = CreateTweet(tweet_data, author_data, parent_tweet, parent_author).execute()

  neo4j.create(tweet, tweet.parent)
