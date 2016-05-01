from summary_mod import get_features
from News_Scraper import HindustanTimes, CNN, CNN_Scraper

import nltk
from collections import defaultdict
from heapq import nlargest

import csv
import os

# Value of k for k-NN
k_neighbors = 8
feature_vec_len = 20
# my_stopwords for "get_features()"
my_stopwords = ['``','--']

training_data = []
# This is the main list containing all training feature_vectors
# [{'feature_vector':['google',''..],'label':'Tech'},{..},..]

#--------------------------------------------------#
def prepareTraining_data():
    nonTechPath = '/Users/sunyambagga/GitHub/NewsClassifier/corpora/non_tech/'
    techPath = '/Users/sunyambagga/GitHub/NewsClassifier/corpora/tech/'
    features = []
    
    print "\nProcessing Non-Tech corpus.."
    for file_name in os.listdir(nonTechPath):
        if '.txt' in file_name:
#            print "Reading file: ", file_name
            with open(nonTechPath+file_name, 'rb') as file:
                tuple = file.readlines()
                
                if len(tuple) == 2:
                    tuple[0] = tuple[0].decode("ascii", errors="ignore")
                    tuple[1] = tuple[1].decode("ascii", errors="ignore")
                    
                    features = get_features(tuple, feature_vec_len, my_stopwords)
                    training_data.append({'feature_vector':features, 'label':'Non-Tech'})

    
    print "Done!\n\nProcessing Tech corpus.."
    for file_name in os.listdir(techPath):
        if '.txt' in file_name:
#            print "Reading file: ", file_name
            with open(techPath+file_name, 'rb') as file:
                tuple = file.readlines()
                
                if len(tuple) == 2:
                    tuple[0] = tuple[0].decode("ascii", errors="ignore")
                    tuple[1] = tuple[1].decode("ascii", errors="ignore")
                    
                    features = get_features(tuple, feature_vec_len, my_stopwords)
                    training_data.append({'feature_vector':features, 'label':'Tech'})
    print "Done!"
#    print training_data

#    with open('learned_features.csv', 'wb') as file:
#        writer = csv.writer(file, delimiter=',', quotechar='"')
#        print "Writing features to CSV"
#        for dict in training_data:
#            writer.writerow([dict['feature_vector'], dict['label']])

#--------------------------------------------------#
prepareTraining_data()

#--------------------------------------------------#
# SVM
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import numpy as np

def SVM():
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
    to_int = {"Tech":1, "Non-Tech":2}

    svm_labels = []
    for dict in training_data:
        svm_labels.append(to_int[dict['label']])

    Y = np.array(svm_labels)

    SVMClassifier = SVC(C=1000000.0)

    SVMClassifier.fit(X, Y)

    # Make test instance compatible form for SVM:
    test_sent = " ".join(test_features)
    test_x = vectorizer.transform([test_sent]).toarray()
    #print "Test Instance:", test_sent
    #print test_x

    if SVMClassifier.predict(test_x)[0] == 2:
        print "SVM thinks it is a Non-Tech article."
        return 0
    else:
        print "SVM thinks it is a Tech article."
        return 1
#--------------------------------------------------#

#--------------------------------------------------#
# k-NN
def k_NN():
    similar = {}

    for i, dict in enumerate(training_data):
        similar[i] = len(set(dict['feature_vector']).intersection(set(test_features)))

    knn = nlargest(k_neighbors, similar, key=similar.get)
#    print knn

    category = {'Tech':0, 'Non-Tech':0}

    for neighbor in knn:
        if training_data[neighbor]['label'] == 'Tech':
            category['Tech'] += 1
        else:
            category['Non-Tech'] += 1

#    print category
    label_knn = nlargest(1, category, key=category.get)[0]
    print "k-NN thinks it is a " + label_knn + " article."

    if label_knn=="Tech":
        return 1
    else:
        return 0

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

def NaiveBayes():
    # Transform training_data for NB:
    training_data_nb = []
    for dict in training_data:
        list_of_words = dict['feature_vector']
        label = dict['label']
        
        training_data_nb.append((list_of_words, label))

    train_features_nb = nltk.classify.apply_features(feature_fn, training_data_nb)

    # trian_features_nb: [({'facebook':True, 'cricket':False..}, 'Tech'), ({..},'Non-Tech'), (..), (..)..]

    #print "Creating Naive Bayes Classifier ...."
    NBClassifier = nltk.NaiveBayesClassifier.train(train_features_nb)
    #print "The possible labels are: ", NBClassifier._labels
    #print NBClassifier.show_most_informative_features(10)
    verdict = NBClassifier.classify(feature_fn(test_features))
    print "NB thinks it is a " + verdict + " article."
    if verdict=="Tech":
        return 1
    else:
        return 0


#--------------------------------------------------#



#--------------------------------------------------#
# Reading test-article from file
test_article_path = '/Users/sunyambagga/GitHub/NewsClassifier/test_articles'
append = ['/Tech/','/Non_Tech/']

nb_predictions = []
svm_predictions = []
knn_predictions = []
my_predictions = []

true_labels = []

for ap in append:
    for a in os.listdir(test_article_path+ap)[1:]:
        print "Inside", a
        with open(test_article_path+ap+a, 'rb') as f:
            article = f.readlines()
            if len(article) == 2:   # Checking if file contains content
                article[0] = article[0].decode("ascii", errors="ignore")
                article[1] = article[1].decode("ascii", errors="ignore")
        # Represent test instance as a feature-vector
        test_features = get_features(article, feature_vec_len, my_stopwords)
#        print "Test article: ", test_features

        d = 0
        
        if '/Tech/' in ap:
            true_labels.append(1)
        if '/Non_Tech/' in ap:
            true_labels.append(0)
    
        nb = NaiveBayes()
        svm = SVM()
        knn = k_NN()
        nb_predictions.append(nb)
        svm_predictions.append(svm)
        knn_predictions.append(knn)

        d += nb + svm + knn
        if d >= 2:
            print "Tech\n\n"
            my_predictions.append(1)
        elif d < 2:
            print "Non-Tech\n\n"
            my_predictions.append(0)




print "\n\n\n\n\n\n"
print "NB: ", nb_predictions
print "\n"
print "SVM:", svm_predictions
print "\n"
print "kNN:", knn_predictions
print "\n"
print "Clas", my_predictions
print "\n"
print "True", true_labels
print "\n"
#print "NB: ", len(nb_predictions)
#print "SVM:", len(svm_predictions)
#print "kNN:", len(knn_predictions)
#print "True", len(true_labels)
#print "\n\n\n\n\n\n"

#--------------------------------------------------#
# Evaluating Classifier:
from sklearn import metrics

print "Confusion Matrix:\n", metrics.confusion_matrix(true_labels, my_predictions)
print "\n\n"
print "k-NN:\n", metrics.classification_report(true_labels, knn_predictions, labels=[0,1], target_names=['Non-Tech','Tech'])
print "k-NN Accuracy:", metrics.accuracy_score(true_labels, knn_predictions)
print "\n\n"
print "SVM:\n", metrics.classification_report(true_labels, svm_predictions, labels=[0,1], target_names=['Non-Tech','Tech'])
print "SVM Accuracy:", metrics.accuracy_score(true_labels, svm_predictions)
print "\n\n"
print "Naive Bayes:\n", metrics.classification_report(true_labels, nb_predictions, labels=[0,1], target_names=['Non-Tech','Tech'])
print "NB Accuracy:", metrics.accuracy_score(true_labels, nb_predictions)
print "\n\n"
print "MyModel:\n", metrics.classification_report(true_labels, my_predictions, labels=[0,1], target_names=['Non-Tech','Tech'])
print "My Accuracy:", metrics.accuracy_score(true_labels, my_predictions)
print "\n\n"

#--------------------------------------------------#



################################################
# Writing test articles

## HindustanTimes
#cnn_url_nontech = 'http://edition.cnn.com/sport'
#cnn_url_tech = 'http://edition.cnn.com/tech'
#cnn_tech_articles = CNN_Scraper(cnn_url_tech, 1)
#print "Wait.."
#cnn_nontech_articles = CNN_Scraper(cnn_url_nontech, 0)
#print "\n\nCNN: Done"
#
#i = 14
## Non-Tech
#for url in cnn_nontech_articles:
#    title = cnn_nontech_articles[url][0]
#    body = cnn_nontech_articles[url][1]
#    article = title + "\n" + body
#    article = article.encode('utf8')
#    with open('/Users/sunyambagga/GitHub/NewsClassifier/test_articles/non_test_'+str(i)+'.txt', 'wb') as file:
#        print "Writing", i
#        file.write(article)
#        i += 1
#
#for url in cnn_tech_articles:
#    title = cnn_tech_articles[url][0]
#    body = cnn_tech_articles[url][1]
#    article = title + "\n" + body
#    article = article.encode('utf8')
#    with open('/Users/sunyambagga/GitHub/NewsClassifier/test_articles/tech_test_'+str(i)+'.txt', 'wb') as file:
#        print "Writing", i
#        file.write(article)
#        i += 1
################################################
################################################
# Writing all test articles into a file
#test_url1 = "http://money.cnn.com/2016/04/18/technology/bill-campbell-intuit-death/index.html" # Only SVM fails
#test_url2 = "http://money.cnn.com/2016/04/08/technology/adobe-emergency-update/index.html" # None fail (k-NN: 5 to 3)
#test_url3 = "http://money.cnn.com/2016/04/20/technology/google-android-lawsuit-europe/index.html" # Badass link
#test_url4 = "http://money.cnn.com/2016/04/19/technology/apple-macbook/index.html" # Badass link
#test_url5 = "http://edition.cnn.com/2016/04/21/football/brazil-neymar-olympics/index.html" # Badass link
#test_url6 = "http://edition.cnn.com/2016/04/20/tennis/french-open-arantxa-sanchez-vicario/index.html" # None fail (k-NN: 7 to 1)
#test_url7 = "http://money.cnn.com/2016/04/18/investing/yahoo-bidders-verizon-aol/index.html" # None fail (k-NN: 7 to 1) #Tech
#test_url8 = "http://money.cnn.com/2016/04/22/technology/apple-china-ibooks-itunes-movies-closed/index.html" #Badass
#test_url9 = "http://money.cnn.com/2016/04/21/technology/comcast-xfinity-cable-app/index.html" #Badass
#test_url10 = "http://money.cnn.com/2016/04/19/technology/intel-layoffs/index.html" #Badass
#test_url11 = "http://edition.cnn.com/2016/04/23/tennis/rafael-nadal-kei-nishikori-barcelona/index.html" #Badass
#test_url12 = "http://edition.cnn.com/2016/04/23/football/fa-cup-anthony-martial-manchester-united-everton/index.html" #Badass
#test_url13 = "http://edition.cnn.com/2016/04/22/golf/tiger-woods-return/index.html" # Badass

#test_urls = [test_url1, test_url2, test_url3, test_url4, test_url5, test_url6, test_url7, test_url8, test_url9, test_url10, test_url11, test_url12, test_url13]

#i = 1
#for url in test_urls:
#    with open('/Users/sunyambagga/GitHub/NewsClassifier/test_articles/test_'+str(i)+'.txt', 'wb') as file:
#        print "Writing ", i
#        i += 1
#        article = CNN(url)
#        article = list(article)
#        article[0] = article[0].encode("ascii", errors="ignore")
#        article[1] = article[1].encode("ascii", errors="ignore")
#        text = article[0] + "\n" + article[1]
#        file.write(text)
################################################




