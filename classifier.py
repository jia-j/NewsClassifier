from summary_mod import get_features
from News_Scraper import HindustanTimes

from collections import defaultdict
from heapq import nlargest

import csv
import os

# Value of k for k-NN
k_neighbors = 8


main_list = []
# This is the main list containing all training feature_vectors
# [{'feature_vector':['google',''..],'label':'Tech'},{..},..]

#--------------------------------------------------#
def prepareMainList():
    nonTechPath = '/Users/sunyambagga/GitHub/NewsClassifier/corpora/nonTech/'
    techPath = '/Users/sunyambagga/GitHub/NewsClassifier/corpora/tech/'
    features = []
    
    for file_name in os.listdir(nonTechPath):
        if '.txt' in file_name:
#            print "Reading file: ", file_name
            with open(nonTechPath+file_name, 'rb') as file:
                tuple = file.readlines()
                tuple[0] = tuple[0].decode("ascii", errors="ignore")
                tuple[1] = tuple[1].decode("ascii", errors="ignore")
                
                features = get_features(tuple, 25)
                main_list.append({'feature_vector':features, 'label':'Non-Tech'})

    print "\nFinished reading Non-Tech corpus!"
    
    for file_name in os.listdir(techPath):
        if '.txt' in file_name:
#            print "Reading file: ", file_name
            with open(techPath+file_name, 'rb') as file:
                tuple = file.readlines()
                tuple[0] = tuple[0].decode("ascii", errors="ignore")
                tuple[1] = tuple[1].decode("ascii", errors="ignore")
                
                features = get_features(tuple, 25)
                main_list.append({'feature_vector':features, 'label':'Tech'})

    print "\nFinished reading Tech corpus!"
#    print main_list

#    with open('latest_features.csv', 'wb') as file:
#        writer = csv.writer(file, delimiter=',', quotechar='"')
#        print "Writing features to CSV"
#        for dict in main_list:
#            writer.writerow([dict['feature_vector'], dict['label']])

#--------------------------------------------------#

#--------------------------------------------------#
# k-NN
def k_NN(main_list, test_features):
    similar = {}

    for i, dict in enumerate(main_list):
        similar[i] = len(set(dict['feature_vector']).intersection(set(test_features)))

    knn = nlargest(k_neighbors, similar, key=similar.get)
    print knn

    category = {'Tech':0, 'Non-Tech':0}

    for neighbor in knn:
        if main_list[neighbor]['label'] == 'Tech':
            category['Tech'] += 1
        else:
            category['Non-Tech'] += 1

    print category
    label_knn = nlargest(1, category, key=category.get)[0]
    return label_knn
#--------------------------------------------------#

#test_url = "http://www.hindustantimes.com/tech/facebook-has-a-new-research-lab-led-by-ex-google-executive/story-7YYln1vKdh3tMihW6rZFNK.html"
test_url = "http://www.hindustantimes.com/tech/use-app-to-avoid-landslide-blocked-roads-in-sikkim-darjeeling/story-mMClbb9cuN0a5zip1mUTmK.html"
#test_url = "http://www.hindustantimes.com/other-sports/dipa-karmakar-becomes-first-indian-gymnast-to-qualify-for-olympics/story-IvvCXJsxkkvt8Mq3p5telN.html"
#test_url = "http://www.hindustantimes.com/india/drinking-beer-not-our-culture-use-water-to-save-lives-first-shiv-sena/story-gvpAmfDPpdlPZve6K8fLoL.html"

article = HindustanTimes(test_url)
article = list(article)
article[0] = article[0].encode("ascii", errors="ignore")
article[1] = article[1].encode("ascii", errors="ignore")

# Prepare training feature vectors
prepareMainList()

# Represent test instance as a feature-vector
test_features = get_features(article, 25)

# Call k-NN algorithm
knn_verdict = k_NN(main_list, test_features)

print "\nk-NN thinks it is a " + knn_verdict + " article."



