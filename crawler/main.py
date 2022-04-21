import tweepy, configparser
from drivers.neo4j.client import Client
from use_cases.search_tweet_data import SearchTweetData

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
tweets = SearchTweetData(client, "bolsonaro").execute()

# save data to db
for tweet in tweets:
  neo4j.create(tweet, tweet.parent)
