import tweepy, json, unicodedata, datetime
# keys and tokens from the Twitter Dev Console
consumer_key = 'VMlB52MoI0CLkSqAuW2gDpAQp'
consumer_secret = '3m0VJlWPU1nysGrG7O33vokDHyECKBamti8etsdE034cxUNW4E'
access_token = '939376477-njZLNYpx0EASsWWDaJbH1o53aqheIYkkML7pOkLq'
access_token_secret = 'e7e8aHfniRrXZx5vrZZjP6yC9vjZzCGlQdl8i3veK7GEA'

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth)

# Using the API object to get tweets from your timeline, and storing it in a variable called public_tweets
#public_tweets = api.home_timeline()
# foreach through all tweets pulled
#result = []
#for tweet in public_tweets:
   # printing the text stored inside the tweet object

temp = api.user_timeline("emmadarif")

startDate = datetime.datetime(2019, 3, 1, 0, 0, 0)
endDate = datetime.datetime(2019, 4, 1, 0, 0, 0)

tweets = []
for tweet in temp:

    if tweet.created_at > startDate and tweet.created_at < endDate:
        tweets.append(tweet)

while temp[-1].created_at > startDate:
    temp = api.user_timeline("emmadarif", max_id = temp[-1].id)
    for tweet in temp:
        if tweet.created_at < endDate and tweet.created_at > startDate:
            tweets.append(tweet)
for tweet in tweets:
    tweetText = unicodedata.normalize('NFKD', tweet.text).encode('ascii','ignore')
    tweetAuthor = unicodedata.normalize('NFKD', tweet.user.screen_name).encode('ascii','ignore')
    tweetDate = str(tweet.created_at)

    print("Tweet: " + tweetText.decode("utf-8"))
    print("Author: " + tweetAuthor.decode("utf-8"))
    print("Created at: " + tweetDate)
    print("\n")



"""
    result.append({
        'text': tweet.text,
        'author_name': tweet.user.screen_name
    })
with open('tweet.json', 'w+') as f:
    json.dump(result, f)
"""
