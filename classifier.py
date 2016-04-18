from summary_mod import get_features

from collections import defaultdict
from heapq import nlargest

import csv
import os

features = []

main_list = []
# This is the main dictionary: {'url':{'feature_vector':[], 'label':'Tech'}..}

#--------------------------------------------------#
def prepareFeatures_csv():
    nonTechPath = '/Users/sunyambagga/GitHub/NewsClassifier/corpora/nonTech/'
    techPath = '/Users/sunyambagga/GitHub/NewsClassifier/corpora/tech/'

    for file_name in os.listdir(nonTechPath):
        if '.txt' in file_name:
            print "Reading file: ", file_name
            with open(nonTechPath+file_name, 'rb') as file:
                tuple = file.readlines()
                tuple[0] = tuple[0].decode("ascii", errors="ignore")
                tuple[1] = tuple[1].decode("ascii", errors="ignore")
                
                features = get_features(tuple, 25)
                main_list.append({'feature_vector':features, 'label':'Non-Tech'})

    print "\n\n"
    
    for file_name in os.listdir(techPath):
        if '.txt' in file_name:
            print "Reading file: ", file_name
            with open(techPath+file_name, 'rb') as file:
                tuple = file.readlines()
                tuple[0] = tuple[0].decode("ascii", errors="ignore")
                tuple[1] = tuple[1].decode("ascii", errors="ignore")
                
                features = get_features(tuple, 25)
                main_list.append({'feature_vector':features, 'label':'Tech'})

    print main_list

    with open('latest_features.csv', 'wb') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"')
        print "Writing features to CSV"
        for dict in main_list:
            writer.writerow([dict['feature_vector'], dict['label']])

    print "\nDONE!"

#prepareFeatures_csv()
#--------------------------------------------------#


#article = HindustanTimes("http://www.hindustantimes.com/tech/facebook-has-a-new-research-lab-led-by-ex-google-executive/story-7YYln1vKdh3tMihW6rZFNK.html")

# k-NN
#test_features = get_features(article, 25)
#print "TEST FEATURES:\n\n\n\n", test_features
#
#similar = {}
#
#for article_url in main_list:
#    similar[article_url] = len(set(main_list[article_url]['feature_vector']).intersection(set(test_features)))
#
#print "SIMILAR DICT:\n\n"
#print similar
#
#knn = nlargest(5, similar, key=similar.get)
#category = defaultdict(int)
#
#for url_neighbor in knn:
#    category[main_list[url_neighbor]['label']] += 1
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
#main_list = defaultdict(int)
#
#for techUrl in tech_summaries:
#    features = get_features(tech_summaries[techUrl], 25)
#    
#    main_list[techUrl] = {'feature_vector':features, 'label':'Tech'}
#
#
#for nontechUrl in nontech_summaries:
#    features = get_features(nontech_summaries[nontechUrl], 25)
#    main_list[nontechUrl] = {'feature_vector':features, 'label':'Non-Tech'}




