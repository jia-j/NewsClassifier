from summary_mod import get_features

from collections import defaultdict
from heapq import nlargest
import csv

#features = []
#main_dict = {}
#
#for website_dict in [w_tech_articles, ny_tech_articles]:
#    print "\n\nInside Tech"
#    for techUrl in website_dict:
#        features = get_features(website_dict[techUrl], 25)
#        main_dict[techUrl] = {'feature_vector':features, 'label':'Tech'}
#
#for website_dict in [w_nontech_articles, ny_nontech_articles]:
#    print "\n\nInside Non-Tech"
#    for nontechUrl in website_dict:
#        features = get_features(website_dict[nontechUrl], 25)
#        main_dict[nontechUrl] = {'feature_vector':features, 'label':'Non-Tech'}
#
#print main_dict
#
#with open('features.csv', 'wb') as file:
#    writer = csv.writer(file, delimiter=',', quotechar='"')
#    print "WRITING TO CSV"
#    for url in main_dict:
#        writer.writerow([main_dict[url]['feature_vector'], main_dict[url]['label']])
#
#print "\nDONE!"
#article = HindustanTimes("http://www.hindustantimes.com/tech/facebook-has-a-new-research-lab-led-by-ex-google-executive/story-7YYln1vKdh3tMihW6rZFNK.html")

# k-NN
#test_features = get_features(article, 25)
#print "TEST FEATURES:\n\n\n\n", test_features
#
#similar = {}
#
#for article_url in main_dict:
#    similar[article_url] = len(set(main_dict[article_url]['feature_vector']).intersection(set(test_features)))
#
#print "SIMILAR DICT:\n\n"
#print similar
#
#knn = nlargest(5, similar, key=similar.get)
#category = defaultdict(int)
#
#for url_neighbor in knn:
#    category[main_dict[url_neighbor]['label']] += 1
#
#print "\n\n\n\n\n"
#print category


# TheHindu
#h_url_nontech = 'http://www.thehindu.com/sport'
#h_url_tech = 'http://www.thehindu.com/sci-tech/'
#tech_summaries = TH_Scraper(h_url_tech, 1)
#
#nontech_summaries = TH_Scraper(h_url_nontech, 0)
#
#features = []
#main_dict = defaultdict(int)
#
#for techUrl in tech_summaries:
#    features = get_features(tech_summaries[techUrl], 25)
#    
#    main_dict[techUrl] = {'feature_vector':features, 'label':'Tech'}
#
#
#for nontechUrl in nontech_summaries:
#    features = get_features(nontech_summaries[nontechUrl], 25)
#    main_dict[nontechUrl] = {'feature_vector':features, 'label':'Non-Tech'}




