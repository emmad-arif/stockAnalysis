import textblob, sys
import json, unicodedata
import urllib, pprint

headlines = []
urls = []
snippets = []
def pullTweets(path):
    with open(path) as json_file:
        data = json.load(json_file)
        #print(data)
        for news in data:
            headline = unicodedata.normalize('NFKD', news['text']).encode('ascii','ignore')
            snippet = news['snippet']
            date = news['publishDate']
            url = news['url']
            type = news['type']
            headlines.append(headline.decode())
            urls.append(url)
            snippets.append(snippet)
            """
            print("Headline: " + headline.decode())
            print("Date: " + date[0:10])
            print("URL: " + url)
            print("TYpe: " + type)
            print("\n")
            sys.stdout.flush()
            """
#            print('Tweet: ' + p['text'])

pullTweets('pulledNYT.json')
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

for snippet in snippets:
    #if "apple" in snippet.lower() :
    print(snippet)
    testimonial = textblob.TextBlob(snippet)
    print(testimonial.sentiment)
    print("\n")
