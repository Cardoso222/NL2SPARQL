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
print('Searching...')

#Case where was born
if (tagged_words[0][1] == 'WRB' and tagged_words[0][0] == 'Where' and tagged_words[1][1] == 'VBN'):
    term = ''
    i = 0
    for word in tagged_words:
        if (word[1] == 'NNP'):
            if (i == 0):
                term += word[0]
            else:
                term += ' ' + word[0]

            i += 1
    
    sparql.whereWasBorn(term)

#Case who
if (tagged_words[0][1] == 'WP'):
    name = ''
    i = 0
    for word in tagged_words:
        if (word[1] == 'NNP'):
            if (i == 0):
                name += word[0]
            else:
                name += ' ' + word[0]
        
            i += 1
    sparql.whoIs(name)

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

            i += 1
            
    sparql.whereIs(place)

#Case what
if (tagged_words[0][1] == 'WP' and tagged_words[0][0] == 'What'):
    term = ''
    i = 0
    for word in tagged_words:
        if (word[1] != 'WP' and word[1] != '.'):
            if (i == 0):
                term += word[0]
            else:
                term += ' ' + word[0]

            i += 1
            
    sparql.whatIs(term)

# case how to cook
if (tagged_words[0][1] == 'WRB' and tagged_words[0][0] == 'How'):
    term = ''
    i = 0
    for word in tagged_words:
        if (word[1] == 'NNP'):
            if (i == 0):
                term += word[0]
            else:
                term += ' ' + word[0]

            i += 1
    
    sparql.howToCook(term)

