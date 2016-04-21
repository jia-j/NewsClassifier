from summary_mod import get_features
from News_Scraper import HindustanTimes

import nltk
from collections import defaultdict
from heapq import nlargest

import csv
import os

# Value of k for k-NN
k_neighbors = 8


training_data = []
# This is the main list containing all training feature_vectors
# [{'feature_vector':['google',''..],'label':'Tech'},{..},..]

#--------------------------------------------------#
def prepareTraining_data():
    nonTechPath = '/Users/sunyambagga/GitHub/NewsClassifier/corpora/nonTech/'
    techPath = '/Users/sunyambagga/GitHub/NewsClassifier/corpora/tech/'
    features = []
    
    for file_name in os.listdir(nonTechPath):
        if '.txt' in file_name:
#            print "Reading file: ", file_name
            with open(nonTechPath+file_name, 'rb') as file:
                tuple = file.readlines()
                
                if len(tuple) == 2:
                    tuple[0] = tuple[0].decode("ascii", errors="ignore")
                    tuple[1] = tuple[1].decode("ascii", errors="ignore")
                    
                    features = get_features(tuple, 25)
                    training_data.append({'feature_vector':features, 'label':'Non-Tech'})

    print "\nFinished reading Non-Tech corpus!"
    
    for file_name in os.listdir(techPath):
        if '.txt' in file_name:
#            print "Reading file: ", file_name
            with open(techPath+file_name, 'rb') as file:
                tuple = file.readlines()
                
                if len(tuple) == 2:
                    tuple[0] = tuple[0].decode("ascii", errors="ignore")
                    tuple[1] = tuple[1].decode("ascii", errors="ignore")
                    
                    features = get_features(tuple, 25)
                    training_data.append({'feature_vector':features, 'label':'Tech'})

    print "\nFinished reading Tech corpus!"
#    print training_data

#    with open('latest_features.csv', 'wb') as file:
#        writer = csv.writer(file, delimiter=',', quotechar='"')
#        print "Writing features to CSV"
#        for dict in training_data:
#            writer.writerow([dict['feature_vector'], dict['label']])

#--------------------------------------------------#
prepareTraining_data()

#--------------------------------------------------#
# Test instance
#test_url = "http://www.hindustantimes.com/tech/facebook-has-a-new-research-lab-led-by-ex-google-executive/story-7YYln1vKdh3tMihW6rZFNK.html"
#test_url = "http://www.hindustantimes.com/tech/use-app-to-avoid-landslide-blocked-roads-in-sikkim-darjeeling/story-mMClbb9cuN0a5zip1mUTmK.html"
#test_url = "http://www.hindustantimes.com/other-sports/dipa-karmakar-becomes-first-indian-gymnast-to-qualify-for-olympics/story-IvvCXJsxkkvt8Mq3p5telN.html"
test_url = "http://www.hindustantimes.com/cricket/lodha-panel-reforms-bcci-appoint-media-veteran-rahul-johri-as-ceo/story-4AhU2Teh8UOT1j9r4bqX4L.html"

#test_url = "http://www.hindustantimes.com/world/blast-rocks-afghan-capital-close-to-state-buildings-us-embassy/story-WLVzg9Va3A4oXsytpsAXbN.html"
#test_url = "http://www.hindustantimes.com/india/drinking-beer-not-our-culture-use-water-to-save-lives-first-shiv-sena/story-gvpAmfDPpdlPZve6K8fLoL.html"

article = HindustanTimes(test_url)
article = list(article)
article[0] = article[0].encode("ascii", errors="ignore")
article[1] = article[1].encode("ascii", errors="ignore")

# Represent test instance as a feature-vector
test_features = get_features(article, 25)
print "Test article: ", test_features
print "\n\n"
#--------------------------------------------------#


#--------------------------------------------------#
# k-NN
def k_NN(training_data, test_features):
    similar = {}

    for i, dict in enumerate(training_data):
        similar[i] = len(set(dict['feature_vector']).intersection(set(test_features)))

    knn = nlargest(k_neighbors, similar, key=similar.get)
    print knn

    category = {'Tech':0, 'Non-Tech':0}

    for neighbor in knn:
        if training_data[neighbor]['label'] == 'Tech':
            category['Tech'] += 1
        else:
            category['Non-Tech'] += 1

    print category
    label_knn = nlargest(1, category, key=category.get)[0]
    return label_knn

# Call k-NN algorithm
knn_verdict = k_NN(training_data, test_features)
print "\nk-NN thinks it is a " + knn_verdict + " article."

#--------------------------------------------------#

#--------------------------------------------------#
# Naive Bayes
def createVocabulary():
    allWords = []
    for dict in training_data:
        allWords.extend(dict['feature_vector'])

#    print len(allWords)

    vocab = nltk.FreqDist(allWords).keys()
    return vocab

def feature_fn(article):
    article = set(article)
    feature_vec_nb = {}

    for word in vocab:
        feature_vec_nb[word] = (word in article)

    return feature_vec_nb

vocab = createVocabulary()
# Transform training_data for NB:
training_data_nb = []

for dict in training_data:
    list_of_words = dict['feature_vector']
    label = dict['label']
    
    training_data_nb.append((list_of_words, label))

train_features_nb = nltk.classify.apply_features(feature_fn, training_data_nb)

# trian_features_nb: [({'facebook':True,'cricket':False..},'Tech'),({},'Non-Tech'),(),()..]

#print "Creating Naive Bayes Classifier ...."
NBClassifier = nltk.NaiveBayesClassifier.train(train_features_nb)
#print "The possible labels are: ", NBClassifier._labels
#print NBClassifier.show_most_informative_features(10)
print "\n\nNB thinks it is a " + NBClassifier.classify(feature_fn(test_features)) + " article.\n"

#--------------------------------------------------#
