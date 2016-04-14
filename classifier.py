from News_Scraper import TH_Scraper, W_Scraper, HindustanTimes
from summary_mod import get_features
from collections import defaultdict
from heapq import nlargest

h_url_nontech = 'http://www.thehindu.com/sport'
h_url_tech = 'http://www.thehindu.com/sci-tech/'
w_url_nontech = 'https://www.washingtonpost.com/sports'
w_url_tech = 'https://www.washingtonpost.com/business/technology/'

# TheHindu
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




# WashingtonPost
tech_summaries = W_Scraper(w_url_tech, 1)
nontech_summaries = W_Scraper(w_url_nontech, 0)

#print tech_summaries
#print "\n\n\n\n\n\n"
#print nontech_summaries

features = []
main_dict = {}

for techUrl in tech_summaries:
    features = get_features(tech_summaries[techUrl], 25)
    main_dict[techUrl] = {'feature_vector':features, 'label':'Tech'}

for nontechUrl in nontech_summaries:
    features = get_features(nontech_summaries[nontechUrl], 25)
    main_dict[nontechUrl] = {'feature_vector':features, 'label':'Non-Tech'}

print main_dict

#article_body = "Since 2011, Facebook has been rolling out translation features backed by artificial intelligence algorithms. The A.I. reads the post or comment, parses what's being said, and then translates it into a hopefully natural-sounding translation at the click of the button. Last year, instead of asking users if they wanted to have a post translated, Facebook started automatically showing translations, and asking if users want to see the original. Now, more and more Facebook posts are automatically translated; 800 million users per month use the translation feature. But behind the scenes, Facebook is running low-level artificial intelligence on all the text uploaded to Facebook, and documenting how you interact with each language."
#
#article_title = "Facebook loves AI"
#article = (article_title, article_body)

article = HindustanTimes("http://www.hindustantimes.com/tech/facebook-has-a-new-research-lab-led-by-ex-google-executive/story-7YYln1vKdh3tMihW6rZFNK.html")

# k-NN
test_features = get_features(article, 25)
print "TEST FEATURES:\n\n\n\n", test_features

similar = {}

for article_url in main_dict:
    similar[article_url] = len(set(main_dict[article_url]['feature_vector']).intersection(set(test_features)))

print "SIMILAR DICT:\n\n"
print similar

knn = nlargest(5, similar, key=similar.get)
category = defaultdict(int)

for url_neighbor in knn:
    category[main_dict[url_neighbor]['label']] += 1

print "\n\n\n\n\n"
print category

