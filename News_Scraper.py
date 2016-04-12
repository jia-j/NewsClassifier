# Extracting main article content from a url, using BeautifulSoup
from bs4 import BeautifulSoup
import urllib2
from cookielib import CookieJar
import requests
import re

#-----------------------------------------------------------#
# The functions will take as input the url and return the article & title_of_article
# For WashingtonPost
def WashingtonPost(url):
    try:
        webpage = urllib2.urlopen(url).read().decode('utf8')
    except:
        return (None, None)

    soup = BeautifulSoup(webpage)

    inside_article = str(soup.find_all('article'))
    soup2 = BeautifulSoup(inside_article, "html.parser")
    #"html.parser" is a crucial argument : http://stackoverflow.com/questions/14822188/dont-put-html-head-and-body-tags-automatically-beautifulsoup

    articleBody = ' '.join(map(lambda x: x.text, soup2.find_all('p')))
    
    return soup.title.text, articleBody


# For TheHindu
def TheHindu(url):
    try:
        webpage = urllib2.urlopen(url).read().decode('utf8')
    except:
        return (None, None)

    soup = BeautifulSoup(webpage)

    # It contains a sub-heading in a div "articleLead"
    sub_heading = ''.join(soup.find("div", {"class" : "articleLead"}).text)
    
    articleBody = ' '.join(map(lambda x: x.text, soup.find_all("p", {"class" : "body"})))
    
    article = sub_heading + articleBody
    return soup.title.text, article

# For Hindustan Times
def HindustanTimes(url):
    try:
        webpage = urllib2.urlopen(url).read().decode('utf8')
    except:
        return (None, None)

    soup = BeautifulSoup(webpage)
    
    article = ' '.join(map(lambda x: x.text, soup.findAll("p")))

    return soup.title.text, article


#-----------------------------------------------------------#

# Main Scraper Function for Washington:
# Tech: It's either switch or innovation
# For tech: dial 1
# For sports: dial 0
def W_Scraper(url, dial=1):
    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
    
    all_content = {}
    
    errors = 0
    for link in soup.find_all('a'):
        try:
            _url = link['href']
            if dial == 1:
                if _url not in all_content and '2016' in _url and 'washington' in _url and ('switch' in _url or 'innovation' in _url) and '.com/video/' not in _url:
                    article = WashingtonPost(_url)
                    if len(article) > 0:
                        all_content[_url] = article
#                    print _url + "  "
            # Sports
            else:
                if _url not in all_content and '2016' in _url and 'washington' in _url:
                    article = WashingtonPost(_url)
                    if len(article) > 0:
                        all_content[_url] = article
#                    print _url + "  "

    
        except:
            errors += 1

    return all_content

#url = "https://www.washingtonpost.com/sports"
#print W_Scraper(url, 0)

# Main Scraper Function for TheHindu:
# For tech: dial 1
# For sports: dial 0
def TH_Scraper(url, dial=1):
    webpage = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(webpage)

    all_content = {}
    errors = 0

    for link in soup.find_all('a'):
        try:
            _url = link['href']
            
            if dial == 1:
                if _url not in all_content and '/sci-tech/' in _url and 'article' in _url:
                    article = TheHindu(_url)
                    if len(article) > 0:
                        all_content[_url] = article
    
            else:
                if _url not in all_content and '/sport/' in _url and 'article' in _url:
                    article = TheHindu(_url)
                    if len(article) > 0:
                        all_content[_url] = article

        except:
            errors += 1

    return all_content

#url = 'http://www.thehindu.com/sport'
#print TH_Scraper(url, 0)
