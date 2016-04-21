from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict
from heapq import nlargest

from nltk.corpus import stopwords
from string import punctuation

# Adding self-created stopwords to the "default_stopwords" list:
file_path = "/Users/sunyambagga/GitHub/NewsClassifier/corpora/my_stopwords.txt"

with open(file_path, 'rb') as file:
    lines = file.readlines()
    # To remove \r tags
    my_stopwords = []
    for line in lines:
        my_stopwords.append(line.rstrip())


default_stopwords = set(stopwords.words('english') + list(punctuation) + my_stopwords)


def calculate_frequencies(sentences_ll, user_stopwords=None):  # sentences_ll is a list of lists
    frequency = defaultdict(int)    # default value : 0
    
    if user_stopwords is not None:
        stopwords = set(user_stopwords).union(default_stopwords)
    else:
        stopwords = default_stopwords
    
    for sentence in sentences_ll:
        for word in sentence:
            word = word.lower()
            if word not in stopwords:
                frequency[word] += 1

    # Normalise frequency
#    max_frequency = max(frequency.values())
#    
#    for word in frequency.keys():
#        frequency[word] /= float(max_frequency)

    return frequency


def summarise(article, n):  # article is a tuple: (title,text)
    title = article[0]
    text = article[1]
    sentences = sent_tokenize(text)
    
    if n > len(sentences):
        return -1

    sentences_ll = []
    for s in sentences:
        words = word_tokenize(s)
        sentences_ll.append(words)

    frequency = calculate_frequencies(sentences_ll)
    rank = defaultdict(int)

    for i, sentence in enumerate(sentences_ll):
        for word in sentence:
            if word in frequency:
                rank[i] += frequency[word]

    id_imp_sents = nlargest(n, rank, key=rank.get)
    sent_ids = sorted(id_imp_sents)

    summary = []
    for i in sent_ids:
        summary.append(sentences[i])

    return summary

def get_features(article, n, user_stopwords=None):  # n is the desired no. of features
    title = article[0]
    text = article[1]
    sentences = sent_tokenize(text)
    
    sentences_ll = []
    for s in sentences:
        words = word_tokenize(s)
        sentences_ll.append(words)

    frequency = calculate_frequencies(sentences_ll, user_stopwords)

    return nlargest(n, frequency, key=frequency.get)



#article_body = "India's Test cricket captain Virat Kohli is the man of the moment - both on and off the field. The right-handed batsman has not only managed to light up the scoreboards with his stellar performance, he has also left behind India's ODI and T20 captain MS Dhoni, who is one of the highest paid brand endorsers in the country, by raking in the moolahs through his bat. According to a Times of India report, Dhoni pockets around Rs 6 crore for placing a Spartan sticker on his bat and Kohli is paid around Rs 8 crore for sticking an MRF logo on the willow. The Delhi batsman also earns around Rs 2 crore for endorsing apparel and shoes on the pitch. Dhoni, however, is ahead with Rs 8 crore when it comes to off-field brand endorsements such as TV ads. Kohli is paid around Rs 5 crore for the brands he endorses."
#
#article_title = "Virat on fire!"
#article = (article_title, article_body)

#print summarise(article, 2)
#print get_features(article, 10, ["Kohli"])
