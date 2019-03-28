import tweepy, json, unicodedata, datetime, sys
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
#keyword1 = "apple"
#keyword2 = "stock"

searchQuery = 'apple AND stock' # Keyword
results = []
new_tweets = api.search(q=searchQuery, rpp=50,
                        #result_type = "recent",
                        lang = "en")
for tweet in new_tweets:
    tweetDate = str(tweet.created_at)
    tweetText = unicodedata.normalize('NFKD', tweet.text).encode('ascii','ignore')
    print(tweetText.decode())
    print(tweetDate)
    print("\n")
    sys.stdout.flush()
    results.append({
        'text': tweet.text,
        'author_name': tweet.user.screen_name,
        'tweet_date' : str(tweet.created_at)
    })

fileName = "pulledTweets" + ".json"
with open(fileName, 'w+') as f:
    json.dump(results, f)
exit()

userID = "cnbc"
#temp = api.user_timeline(userID)

startDate = datetime.datetime(2019, 1, 1, 0, 0, 0)
endDate = datetime.datetime(2019, 2, 1, 1, 0, 0)

tweets = []
result = []
i = 0
for tweet in temp:
    tweetDate = str(tweet.created_at)
    tweetText = unicodedata.normalize('NFKD', tweet.text).encode('ascii','ignore')
    print(tweetText)
    print(tweetDate)

    sys.stdout.flush()
    result.append({
        'text': tweet.text,
        'author_name': tweet.user.screen_name,
        'tweet_date' : str(tweet.created_at)
    })
"""
while True:
    temp = api.user_timeline(userID, max_id = temp[-1].id)
    for tweet in temp:
        i+=1
        print(str(i))
        tweetDate = str(tweet.created_at)
        tweetText = unicodedata.normalize('NFKD', tweet.text).encode('ascii','ignore')
        print(tweetText)
        print(tweetDate)
        sys.stdout.flush()
"""

fileName = "pulledTweets" + ".json"
with open(fileName, 'w+') as f:
    json.dump(result, f)
"""
    print("Tweet: " + tweetText.decode("utf-8"))
    print("Author: " + tweetAuthor.decode("utf-8"))
    print("Created at: " + tweetDate)
    print("\n")

"""

"""
    result.append({
        'text': tweet.text,
        'author_name': tweet.user.screen_name
    })
with open('tweet.json', 'w+') as f:
    json.dump(result, f)
"""
