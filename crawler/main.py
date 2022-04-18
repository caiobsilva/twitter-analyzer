import tweepy, configparser, json
from entities.tweet import Tweet
from entities.user import User

# read authentication credentials
config = configparser.RawConfigParser()
config.read('.env')

bearer_token = config['twitter']['bearer_token']

# authenticate credentials with twitter API
client = tweepy.Client(bearer_token=bearer_token)

# get tweets
tweets = client.search_recent_tweets(
  query='spfc',
  tweet_fields=['created_at'],
  expansions='author_id'
)

# create users dict
users = { u["id"]: u for u in tweets.includes['users'] }

for tweet in tweets.data:
  # check if tweet has an author
  user = users[tweet.author_id] if users[tweet.author_id] else None
  if user == None:
    raise Exception("Missing author")

  author = User(user.id, user.name, user.username)
  tweet = Tweet(tweet.id, author, tweet.text, tweet.created_at)
