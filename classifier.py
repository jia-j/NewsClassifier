from News_Scraper import TH_Scraper, W_Scraper, HindustanTimes
from summary_mod import get_features
from collections import defaultdict

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




# WASHINGTON
tech_summaries = W_Scraper(w_url_tech, 1)

nontech_summaries = W_Scraper(w_url_nontech, 0)

features = []
main_dict = defaultdict(int)

for techUrl in tech_summaries:
    features = get_features(tech_summaries[techUrl], 25)
    
    main_dict[techUrl] = {'feature_vector':features, 'label':'Tech'}


for nontechUrl in nontech_summaries:
    features = get_features(nontech_summaries[nontechUrl], 25)
    main_dict[nontechUrl] = {'feature_vector':features, 'label':'Non-Tech'}

print main_dict

#article = "The first international conference on the subject of gravitational wave (GW) astronomy after the discovery of gravitational waves was announced, in February, was held recently at International Centre for Theoretical Sciences (ICTS), Bengaluru. Preceded by a discussion meeting which was exclusively for experts in the field, the conference entitled 'Future of Gravitational Wave Astronomy,' aimed at setting down future paths for gravitational wave researchers. Speaking to this correspondent along the sidelines of the conference, Dr P Ajith of ICTS, the organiser of the conference said, 'The big discovery [of gravitational waves], made last year and announced in February, essentially marks the end of an era - the quest for the detection of gravitational waves. It has also opened out a new branch of astronomy. Now, the idea is to make detection of gravitational waves a tool of gravitational wave astronomy. This can test our understanding of fundamental physics, astronomy, cosmology etc. It marks the beginning of a new era.'"
#
#
#
## k-NN
#test_features = get_features(article, 25)
#
#similar = defaultdict(int)
#
#for article_url in main_dict:
#    similar[article_url] = len(set(main_dict[article_url]['feature_vector']).intersection(set(test_features)))
#
#print similar




