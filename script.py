from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords


result = []
words = nltk.word_tokenize("who is Caetano Veloso?")
sTwords = stopwords.words('english')

for word in words:
    if word not in sTwords:
        result.append(word)

print(result)
print(nltk.pos_tag(words))
