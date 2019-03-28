import textblob, sys
import json, unicodedata
import urllib, pprint


texts = []
def pullTweets(path):
    with open(path) as json_file:
        data = json.load(json_file)
        #print(data)
        for tweet in data:
            text = unicodedata.normalize('NFKD', tweet['text']).encode('ascii','ignore')

            texts.append(text.decode())
            """
            print("Headline: " + headline.decode())
            print("Date: " + date[0:10])
            print("URL: " + url)
            print("TYpe: " + type)
            print("\n")
            sys.stdout.flush()
            """
#            print('Tweet: ' + p['text'])

pullTweets('pulledTweets.json')
"""
string = ""
content=urllib.request.urlopen(urls[0])


soup=BeautifulSoup(content)
t=soup.find({'class':'sory-body-text'})
print (t.text)
exit()
for line in content:
    string = string + (line.decode())

print(string)
"""

for text in texts:
    print(text)
    testimonial = textblob.TextBlob(text)
    print(testimonial.sentiment)
    print("\n")
