from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
import sparql

search = raw_input("Search:")
processedWords = []
words = nltk.word_tokenize(search)
sTwords = stopwords.words('english')

#Removing stopwords
for word in words:
    if word not in sTwords:
        processedWords.append(word)

tagged_words = nltk.pos_tag(processedWords)

#Case who
print('Searching...')
if (tagged_words[0][1] == 'WP'):
    name = ''
    i = 0
    for word in tagged_words:
        if (word[1] == 'NNP'):
            if (i == 0):
                name += word[0]
            else:
                name += ' ' + word[0]
        
            i = i + 1
    sparql.whois(name)

#Case where
if (tagged_words[0][1] == 'WRB'):
    place = ''
    i = 0
    for word in tagged_words:
        if (word[1] != 'WRB' and word[1] != '.'):
            if (i == 0):
                place += word[0]
            else:
                place += ' ' + word[0]

            i = i + 1
            
    sparql.whereis(place)

