import urllib.error

import nltk
from nltk.corpus import stopwords

import sparql


def ensure_nltk_data():
    resources = [
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
        ("taggers/averaged_perceptron_tagger_eng", "averaged_perceptron_tagger_eng"),
    ]
    for path, name in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name, quiet=True)


def extract_proper_nouns(tagged_words):
    return " ".join(word for word, tag in tagged_words if tag == "NNP")


def extract_after_question_word(tagged_words):
    return " ".join(
        word for word, tag in tagged_words if tag not in ("WRB", "WP", ".")
    )


def main():
    ensure_nltk_data()

    search = input("Search: ")
    words = nltk.word_tokenize(search)
    stop_words = stopwords.words("english")
    processed_words = [word for word in words if word not in stop_words]
    tagged_words = nltk.pos_tag(processed_words)

    if not tagged_words:
        print("Could not understand the question.")
        return

    print("Searching...")
    first_word, first_tag = tagged_words[0]

    try:
        if (
            first_tag == "WRB"
            and first_word == "Where"
            and len(tagged_words) > 1
            and tagged_words[1][1] == "VBN"
        ):
            sparql.whereWasBorn(extract_proper_nouns(tagged_words))
        elif first_word == "How":
            sparql.howToCook(extract_proper_nouns(tagged_words))
        elif first_tag == "WRB":
            sparql.whereIs(extract_after_question_word(tagged_words))
        elif first_word == "What":
            sparql.whatIs(extract_after_question_word(tagged_words))
        elif first_tag == "WP":
            sparql.whoIs(extract_proper_nouns(tagged_words))
        else:
            print("Question type not supported.")
    except urllib.error.HTTPError as e:
        print("DBpedia is unavailable right now (HTTP %s). Try again later." % e.code)


if __name__ == "__main__":
    main()
