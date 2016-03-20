from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation

from collections import defaultdict

class Summariser:

    def __init__(self):
        self.stopwords = set(stopwords.words('english') + list(punctuation))

    def calculate_frequencies(self, sentences):
        frequency = defaultdict(int)    # default value:0

        for sentence in sentences:
            for word in sentence:
                if word not in self.stopwords:
                    frequency[word] += 1

        # Get in range: 0 to 1
        max_frequency = max(frequency.values())
        
        for word in frequency.keys():
            frequency[word] /= float(max_frequency)
        return frequency



text = "Marlon Samuels is stumped here and Sri Lanka sense a slight sniff. West Indies and Marlon still have the upper hand but one more wicket could make things interesting here. I don't think Sri Lanka is going to win this one. Marlon is injured, we will have to wait and see what happens!"
sent = sent_tokenize(text)
sentences = []
for s in sent:
    sentences.append(word_tokenize(s))

# sentences is a list of lists: [["I", "dont"..],["Gayle", "is"..]]
#print sentences

obj = Summariser()
print obj.calculate_frequencies(sentences)