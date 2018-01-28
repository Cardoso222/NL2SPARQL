from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords


# pre processamento para sparql, dps buscar no dbpedia
# consultas como: qual a capital da bahia ?


result = []

words = nltk.word_tokenize("who is Caetano Veloso?")

sTwords = stopwords.words('english')

for word in words:
    if word not in sTwords:
        result.append(word)

print(result)
print(nltk.pos_tag(words))
     
# file = open("result.txt","w") 
# # file.write(','.join(map(str, posTagger.tag(result)))) 

