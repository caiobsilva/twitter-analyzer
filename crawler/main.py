import tweepy, configparser, json
from entities.tweet import Tweet
from entities.user import User
from drivers.neo4j.client import Client

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
  query="spfc",
  tweet_fields=["created_at"],
  max_results=10,
  expansions="author_id"
)

# create users dict
users = { u["id"]: u for u in tweets.includes["users"] }

for tweet in tweets.data:
  # check if tweet has an author
  user = users[tweet.author_id] if users[tweet.author_id] else None
  if user == None:
    raise Exception("Missing author")

  author = User(user.id, user.name, user.username)
  tweet = Tweet(tweet.id, author, tweet.text, tweet.created_at)

  neo4j.create(tweet)
