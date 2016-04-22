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
        print "Failed urlopen()"
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

# For TheNewYorkTimes
def NYtimes(url):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    webpage = opener.open(url).read().decode('utf8')

    # Gives HTTP infinite loop error on using: webpage = urllib2.urlopen(url).read().decode('utf8')
    # http://stackoverflow.com/questions/9926023/handling-rss-redirects-with-python-urllib2
    
    soup = BeautifulSoup(webpage)

    a_list_of_tags = soup.find_all("p", {"class" : "story-body-text story-content"})

    articleBody = ' '.join(map(lambda x: x.text, a_list_of_tags))
    
    return soup.title.text, articleBody

# For CNN
def CNN(url):
    try:
        webpage = urllib2.urlopen(url).read().decode('utf8')
    except:
        return (None, None)

    soup = BeautifulSoup(webpage)
    
    # Article is inside <p> tags for money.cnn {except the last few <p> tags}
    if "money.cnn" in url:
        all_p_tags = []
        for tag in soup.findAll("p"):
            all_p_tags.append(tag)

        article = ""
        for x in all_p_tags[:-2]:
            article += x.text

    # Article inside <p class="zn-body__paragraph"> for edition.cnn
    elif "edition.cnn" in url:
        first_sent = soup.find("p", {"class" : "zn-body__paragraph"}).text
        rest_of_article = " ".join(map(lambda x: x.text, soup.find_all("div", {"class" : "zn-body__paragraph"})))
        article = first_sent + " " + rest_of_article
    
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
    
    reg_exp = r'\/\?.*'
    
    errors = 0
    for link in soup.find_all('a'):
        try:
            _url = link['href']
            # Clip the URL:
            _url = re.sub(reg_exp, "/", _url)
            
            if dial == 1:
                if _url not in all_content and '2016' in _url and 'washington' in _url and ('switch' in _url or 'innovation' in _url) and '.com/video/' not in _url:
#                    print "Trying to scrape Tech: ", _url
                    article = WashingtonPost(_url)
                    if len(article) > 0:
                        all_content[_url] = article
#                    print _url + "  "
            # Sports
            else:
                if _url not in all_content and '2016' in _url and 'washington' in _url:
#                    print "Trying to scrape Non-Tech: ", _url
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


# Main Scraper Function for NYTimes:
# For tech: dial 1
# For sports: dial 0
def NYT_Scraper(url, dial=1):
    webpage = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(webpage)

    all_content = {}
    errors = 0
    exp = r'.html\?.*'
    
    for link in soup.find_all('a'):
        try:
            _url = link['href']
            
            if dial == 1:
                if '2016' in _url and '/technology/' in _url:
                    # Clip the URL:
                    _url = re.sub(exp, ".html", _url)
                    if _url not in all_content:
                        article = NYtimes(_url)
#                        print _url
                        if len(article) > 0:
                            all_content[_url] = article
    
            else:
                if '2016' in _url and '/sports/' in _url:
                    # Clip the URL:
                    _url = re.sub(exp, ".html", _url)
                    if _url not in all_content:
                        article = NYtimes(_url)
                        if len(article) > 0:
                            all_content[_url] = article

        except:
            errors += 1

    return all_content


#url = 'http://www.nytimes.com/pages/sports/index.html '
#print NYT_Scraper(url, 0)

# Main Scraper Function for HindustanTimes:
# For tech: dial 1
# For sports: dial 0
def HT_Scraper(url, dial=1):
    webpage = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(webpage)

    all_content = {}
    errors = 0
    exp = r'.html\?.*'
    
    for link in soup.find_all('a'):
        try:
            _url = link['href']
            
            if dial == 1:
                if 'story-' in _url and '/tech' in _url and '/photos/' not in _url and '/videos/' not in _url:
                    if _url not in all_content:
                        article = HindustanTimes(_url)
#                        print _url + "\n"
                        if len(article) > 0:
                            all_content[_url] = article
    
            else:
                if 'story-' in _url and ('/other-sports/' in _url or '/cricket/' in _url or '/football/' in _url or '/tennis/' in _url) and '/photos/' not in _url and '/videos/' not in _url:
                    if _url not in all_content:
                        article = HindustanTimes(_url)
                        if len(article) > 0:
                            all_content[_url] = article

        except:
            errors += 1

    return all_content


#url = 'http://www.hindustantimes.com/tech/'
#print HT_Scraper(url, 1)
