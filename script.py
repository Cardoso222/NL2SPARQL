from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
import sparql

search = raw_input("Search:")
result = []
words = nltk.word_tokenize(search)
sTwords = stopwords.words('english')

for word in words:
    if word not in sTwords:
        result.append(word)

tagged_words = nltk.pos_tag(words)


#caso seja who
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
