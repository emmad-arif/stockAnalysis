#secret: rh7VgYz9XSF06Eq0
#key: eW7fXnx8ahNckgjfAPR0VTLFjNHcIciA
import math, sys
import json, requests
from pprint import pprint
import time
keyword= 'apple stock'     # e.g. 'tesla'
startDate = '20190101'  # e.g. '20190321'
endDate = '20190115'    # e.g. '20190321'

query= 'fq=' + keyword + '&begin_date=' + startDate + '&end_date=' + endDate
#query = 'q=tesla&page=1&sort=newest'

page = 0

maxPages = 0
result = []
while page <= maxPages:
    #print(str(page))

    url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?' + query + '&page='+ str(page) +'&sort=newest&api-key=eW7fXnx8ahNckgjfAPR0VTLFjNHcIciA'
    time.sleep(6)
    resp = requests.get(url)
    data = json.loads(resp.text)
    #pprint(data)
    #exit()
    #sys.stdout.flush()
    numOfResponses = data['response']['meta']['hits']
    maxPages = math.ceil(numOfResponses/10)
    #exit()
    #pprint(data)

    #pprint(data['response'])
    for key in data['response']['docs']:
        try:
            text = key['headline']['main']
        except:
            text = ""
        try:
            publishDate = key['pub_date'][0:10]
        except:
            publishDate = ""
        try:
            type = key['type_of_material']
        except:
            type = ""
        try:
            url = key['web_url']
        except:
            url = ""
        try:
            lead_paragraph = key['lead_paragraph']
        except:
            lead_paragraph = ""
        try:
            snippet = key['snippet']
        except:
            snippet = ""

        result.append({
            'text': text,
            'publishDate': publishDate,
            'type' : type,
            'url' : url,
            'lead_paragraph' : lead_paragraph,
            'snippet' : snippet
        })

        print ("Headline: " + text)
        print("Date: " + publishDate)
        print("URL: " + url)
        print("Type: " + type)
        print("Lead: " + lead_paragraph)
        print('Snippet: ' + snippet)
        print("\n")
        sys.stdout.flush()
    page+=1

fileName = "pulledNYT" + ".json"
with open(fileName, 'w+') as f:
    json.dump(result, f)
