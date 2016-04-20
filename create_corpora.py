from News_Scraper import TH_Scraper, W_Scraper, NYT_Scraper, HT_Scraper
import csv

def createCorpora():
    
    techCount = 56
    nontechCount = 1
    tech_path = '/Users/sunyambagga/GitHub/NewsClassifier/corpora/tech/'
    nontech_path = '/Users/sunyambagga/GitHub/NewsClassifier/corpora/non_tech/'

    # WashingtonPost
    w_url_nontech = 'https://www.washingtonpost.com/sports'
    w_url_tech = 'https://www.washingtonpost.com/business/technology/'
    w_tech_articles = W_Scraper(w_url_tech, 1)
    w_nontech_articles = W_Scraper(w_url_nontech, 0)
    print "\n\nWashington: Done"

    # NYTimes
    ny_url_nontech = 'http://www.nytimes.com/pages/sports/index.html'
    ny_url_tech = 'http://www.nytimes.com/pages/technology/index.html'
    ny_tech_articles = NYT_Scraper(ny_url_tech, 1)
    ny_nontech_articles = NYT_Scraper(ny_url_nontech, 0)
    print "\n\nNYTimes: Done"

    # HindustanTimes
    ht_url_nontech = 'http://www.hindustantimes.com/sports/'
    ht_url_tech = 'http://www.hindustantimes.com/tech/'
    ht_tech_articles = HT_Scraper(ht_url_tech, 1)
    ht_nontech_articles = HT_Scraper(ht_url_nontech, 0)
    print "\n\nHindustanTimes: Done"
    
    # Creating corpora by writing to file
    # Non-Tech
    for url in w_nontech_articles:
        title = w_nontech_articles[url][0]
        body = w_nontech_articles[url][1]
        article = title + "\n" + body
        article = article.encode('utf8')
        with open(nontech_path+'washington_'+str(nontechCount)+'.txt', 'wb') as file:
            file.write(article)
            nontechCount += 1

    for url in ny_nontech_articles:
        title = ny_nontech_articles[url][0]
        body = ny_nontech_articles[url][1]
        article = title + "\n" + body
        article = article.encode('utf8')
        
        with open(nontech_path+'nytimes_'+str(nontechCount)+'.txt', 'wb') as file:
            file.write(article)
            nontechCount += 1

    for url in ht_nontech_articles:
        title = ht_nontech_articles[url][0]
        body = ht_nontech_articles[url][1]
        article = title + "\n" + body
        article = article.encode('utf8')
        with open(nontech_path+'ht_'+str(nontechCount)+'.txt', 'wb') as file:
            file.write(article)
            nontechCount += 1


    # Tech
    for url in w_tech_articles:
        title = w_tech_articles[url][0]
        body = w_tech_articles[url][1]
        article = title + "\n" + body
        article = article.encode('utf8')
        with open(tech_path+'washington_'+str(techCount)+'.txt', 'wb') as file:
            file.write(article)
            techCount += 1

    for url in ny_tech_articles:
        title = ny_tech_articles[url][0]
        body = ny_tech_articles[url][1]
        article = title + "\n" + body
        article = article.encode('utf8')
        with open(tech_path+'nytimes_'+str(techCount)+'.txt', 'wb') as file:
            file.write(article)
            techCount += 1

    for url in ht_tech_articles:
        title = ht_tech_articles[url][0]
        body = ht_tech_articles[url][1]
        article = title + "\n" + body
        article = article.encode('utf8')
        with open(tech_path+'ht_'+str(techCount)+'.txt', 'wb') as file:
            file.write(article)
            techCount += 1


createCorpora()
