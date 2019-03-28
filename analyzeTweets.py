import textblob
import json, unicodedata

def pullTweets(path):
    with open(path) as json_file:
        data = json.load(json_file)
        #print(data)
        for tweet in data:
            tweetText = unicodedata.normalize('NFKD', tweet['text']).encode('ascii','ignore')
            print("Tweet: " + tweetText.decode())
            print("Date: " + tweet['tweet_date'])
            print("\n")
#            print('Tweet: ' + p['text'])

pullTweets('jimcramer.json')
