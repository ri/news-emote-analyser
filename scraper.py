from selenium import webdriver
from lxml import html
import requests
import re
from collections import OrderedDict


def formatheadline(headline):
  print(headline)
  return re.sub('\s+',' ', headline.lstrip())

def uniquelist(l):
    return list(filter(None, OrderedDict.fromkeys(l)))

def getheadlines(url, xpath, remove):
    client = requests.get(url)
    content = client.content.decode('UTF-8')
    elements = html.fromstring(content)

    if remove:
      for elem in elements.xpath(remove):
        elem.drop_tree()

    return uniquelist([formatheadline(h.text_content()) for h in elements.xpath(xpath)])

def getheadlines_JS(url, xpath):
    browser = webdriver.PhantomJS()
    tree = browser.get(url)
    elements = browser.find_elements_by_xpath(xpath)
    return uniquelist([formatheadline(h.text) for h in elements])
