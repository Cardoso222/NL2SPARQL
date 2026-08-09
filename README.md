# NL2SPARQL
Application to convert Natural Language to SPARQL

![Alt Text](https://media.giphy.com/media/xUNd9MNbpAXrE3QDU4/giphy.gif)

## Example of Searches

### Search: Where was born Caetano Veloso?
`Brazil`

`Santo Amaro, Bahia`

### Search: Where is London Eye?
`London Borough of Lambeth`

### Search: Who is Caetano Veloso?
`músico, produtor, arranjador e escritor brasileiro`

### Search: What is Bitcoin?
`moeda digital descentralizada`

### Search: How to cook Brigadeiro?
`Doce típico da confeitaria brasileira`

`Ingredientes: Sweetenedcondensed milk,butterandcocoa powder`

## Requirements

Python 3.9+

## Download all dependencies

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

NLTK data (tokenizer, stopwords, POS tagger) is downloaded automatically on first run.

## Running
`python main.py`
