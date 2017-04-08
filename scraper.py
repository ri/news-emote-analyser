from selenium import webdriver
from lxml import html
import requests
import re
from collections import OrderedDict


def formatheadline(headline): return re.sub('\s+',' ', headline.lstrip())

def uniquelist(l):
    return list(OrderedDict.fromkeys(l))

def getheadlines(url, xpath):
    client = requests.get(url)
    elements = html.fromstring(client.content)
    return uniquelist([formatheadline(h.text_content()) for h in elements.xpath(xpath)])

def getheadlines_JS(url, xpath):
    browser = webdriver.PhantomJS()
    tree = browser.get(url)
    elements = browser.find_elements_by_xpath(xpath)
    return uniquelist([formatheadline(h.text) for h in elements])
