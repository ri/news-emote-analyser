
# coding: utf-8

# In[69]:

import json
import time
from scraper import getheadlines, getheadlines_JS
from textanalyser import generatesentiment
import boto
from time import gmtime, strftime
import sys


# In[70]:

def generateheadlinefile(source_file, output_file, s3key, scraperfn):
    with open(source_file) as data_file:
        sources = json.load(data_file)
        data = {}
        data["time"] = time.strftime("%c %Z")
        data["news-data"] = []

    for source in sources:
        headlines = scraperfn(source["url"], source["xpath"])
        sentiments = [generatesentiment("headline", headline) for headline in headlines]
        print(sentiments)

        data["news-data"].append({
            "name": source["name"],
            "sentiments": sentiments
        })

#     with open(output_file, 'w') as outfile:
#         json.dump(data, outfile)

    filename = strftime("%Y-%m-%d", gmtime())
    s3 = boto.connect_s3()
    bucket = s3.create_bucket('data.newsemote')
    key = bucket.new_key(s3key + '/' + filename + '.json')
    key.set_contents_from_string(json.dumps(data))
    key.set_acl('public-read')

    #keep copy of file in latest.json
    latest = bucket.new_key(s3key + '/latest.json')
    latest.set_contents_from_string(json.dumps(data))
    latest.set_acl('public-read')

    #retrieve files in bucket
    files = bucket.list(prefix=s3key)
    files = sorted(files, key=lambda k: k.last_modified, reverse=True)
    filtered = [f for f in files if f.name != s3key + '/latest.json' and f.name != 'last7.json']
    filtered = filtered[:7]
    filelist = [file.name for file in filtered]
    print(filelist)

    #write to list file
    latestlist = bucket.new_key(s3key + '/last7.json')
    latestlist.set_contents_from_string(json.dumps(filelist))
    latestlist.set_acl('public-read')


# In[71]:

def au():
  generateheadlinefile('data/news_sources_au.json', 'data-au.json', "au", getheadlines)

def us():
  generateheadlinefile('data/news_sources_us.json', 'data-us.json', 'us', getheadlines_JS)

def default():
  au()
  us()

run_options = {
  'au' : au,
  'us' : us,
  'all' : default
}

try:
  run = sys.argv[1]
except IndexError:
  run = 'all'

run_options[run]()


# In[ ]:



