from summary_mod import get_features
from News_Scraper import HindustanTimes, CNN

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
                    
                    features = get_features(tuple, 20)
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
                    
                    features = get_features(tuple, 20)
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
################################################
# Successful:
#test_url = "http://www.hindustantimes.com/tech/use-app-to-avoid-landslide-blocked-roads-in-sikkim-darjeeling/story-mMClbb9cuN0a5zip1mUTmK.html"
#test_url = "http://www.hindustantimes.com/tech/google-s-parent-alphabet-results-hit-by-rising-traffic-costs-strong-dollar/story-CF5eP29bZ83zJ7Ul9RcMPN.html"
#test_url = "http://www.hindustantimes.com/other-sports/dipa-karmakar-becomes-first-indian-gymnast-to-qualify-for-olympics/story-IvvCXJsxkkvt8Mq3p5telN.html"
#test_url = "http://www.hindustantimes.com/football/epl-sanchez-settles-arsenal-nerves-with-a-brace-to-sink-west-brom/story-y3YZKnxase32YM7KmrmRrK.html"
#test_url = "http://www.hindustantimes.com/tennis/boris-becker-hits-out-at-andy-murray-over-doping-comments/story-A2e8p128IZlq456uyyklCO.html"
################################################

################################################
# Some Issue:
#test_url = "http://edition.cnn.com/2016/04/16/tech/beam-inflatable-habitat-iss-irpt/index.html"
#test_url = "http://www.hindustantimes.com/cricket/lodha-panel-reforms-bcci-appoint-media-veteran-rahul-johri-as-ceo/story-4AhU2Teh8UOT1j9r4bqX4L.html"
#test_url = "http://www.hindustantimes.com/world/blast-rocks-afghan-capital-close-to-state-buildings-us-embassy/story-WLVzg9Va3A4oXsytpsAXbN.html"
#test_url = "http://www.hindustantimes.com/india/drinking-beer-not-our-culture-use-water-to-save-lives-first-shiv-sena/story-gvpAmfDPpdlPZve6K8fLoL.html"
################################################

################################################
# Champion links:
#test_url = "http://money.cnn.com/2016/04/18/technology/bill-campbell-intuit-death/index.html" # Only SVM fails
#test_url = "http://money.cnn.com/2016/04/08/technology/adobe-emergency-update/index.html" # None fail (k-NN: 5 to 3)
#test_url = "http://money.cnn.com/2016/04/20/technology/google-android-lawsuit-europe/index.html" # Badass link
#test_url = "http://money.cnn.com/2016/04/19/technology/apple-macbook/index.html" # Badass link
#test_url = "http://edition.cnn.com/2016/04/21/football/brazil-neymar-olympics/index.html" # Badass link
#test_url = "http://edition.cnn.com/2016/04/20/tennis/french-open-arantxa-sanchez-vicario/index.html" # None fail (k-NN: 7 to 1)
#test_url = "http://money.cnn.com/2016/04/18/investing/yahoo-bidders-verizon-aol/index.html" # None fail (k-NN: 6 to 2) #Tech
#test_url = "http://www.hindustantimes.com/tech/facebook-has-a-new-research-lab-led-by-ex-google-executive/story-7YYln1vKdh3tMihW6rZFNK.html" # None fail (k-NN: 6 to 2) #Tech
#test_url = "http://www.hindustantimes.com/cricket/india-to-play-its-first-day-night-test-against-nz-in-2016-anurag-thakur/story-QspGDULlJWX0EUo3S7xG8H.html" # Badass link


################################################

#article = CNN(test_url)
article = HindustanTimes(test_url)
article = list(article)
article[0] = article[0].encode("ascii", errors="ignore")
article[1] = article[1].encode("ascii", errors="ignore")

# Represent test instance as a feature-vector
test_features = get_features(article, 20)
#print "Test article: ", test_features
#print "\n\n"
#--------------------------------------------------#

from sklearn.feature_extraction.text import CountVectorizer 

from sklearn.svm import SVC

import numpy as np



svm_training_data = []



for dict in training_data:

    words = dict['feature_vector']

    sentence = " ".join(words)

    svm_training_data.append(sentence)



#print svm_training_data

# [u'cricket lanka herath sri spinner board time matches wickets world internationals t20 muralitharan saying endeavours en retired twenty20 quoted feel', u'rosberg chinese pole qualifying champion grid hamilton world mercedes position quicker vettel due prix set finn carrying clocked winner raikkonen', ..]



vectorizer = CountVectorizer(min_df=1)

X = vectorizer.fit_transform(svm_training_data)

X = X.toarray()

#print "\n\n"

#print X.toarray()

vocabulary_svm = vectorizer.get_feature_names()



# Converting labels "Tech"/"Non-Tech" to integers

to_int = {"Tech":1, "Non-Tech":212}

svm_labels = []

for dict in training_data:

    svm_labels.append(to_int[dict['label']])



Y = np.array(svm_labels)



SVMClassifier = SVC(C=1000000.0, gamma=0.0)

SVMClassifier.fit(X, Y)



# Convert test instance in the compatible form for SVM:

test_sent = " ".join(test_features)

test_x = vectorizer.transform([test_sent]).toarray()

print "Test Instance:", test_sent

#print test_x



#for list in test_x:

#    for i in list:

#        if i == 1:

#            print index(list)



print SVMClassifier.predict(test_x)

print "\n\n\n\n"


















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

##--------------------------------------------------#
## k-Means clustering
#kmeans_path = '/Users/sunyambagga/GitHub/NewsClassifier/corpora/kmeans/'
#
#doc_corpus = []
#for file_name in os.listdir(kmeans_path):
#        if '.txt' in file_name:
#            print "Reading file: ", file_name
#            with open(kmeans_path+file_name, 'rb') as file:
#                tuple = file.readlines()
##                print tuple
#                if len(tuple) == 2:
#                    tuple[0] = tuple[0].decode("ascii", errors="ignore")
#                    tuple[1] = tuple[1].decode("ascii", errors="ignore")
#                    article = tuple[0] + tuple[1]
#
#                    doc_corpus.append(article)
#
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.cluster import KMeans
#
#vectorizer = TfidfVectorizer(max_df=0.5,min_df=2,stop_words='english')
#X = vectorizer.fit_transform(doc_corpus)    # X is a matrix where each row is a vector representing an article
#km = KMeans(n_clusters = 5, init = 'k-means++', max_iter = 100, n_init = 1, verbose = True)
#km.fit(X)
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

# trian_features_nb: [({'facebook':True, 'cricket':False..}, 'Tech'), ({},'Non-Tech'), (), ()..]

#print "Creating Naive Bayes Classifier ...."
NBClassifier = nltk.NaiveBayesClassifier.train(train_features_nb)
#print "The possible labels are: ", NBClassifier._labels
#print NBClassifier.show_most_informative_features(10)
print "\n\nNB thinks it is a " + NBClassifier.classify(feature_fn(test_features)) + " article.\n"

#--------------------------------------------------#
