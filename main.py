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


def parse_question(search):
    """Classify a question and extract its subject.

    Returns an (intent, term) tuple; intent is None when the question
    is empty or not supported.
    """
    words = nltk.word_tokenize(search)
    stop_words = stopwords.words("english")
    processed_words = [word for word in words if word not in stop_words]
    tagged_words = nltk.pos_tag(processed_words)

    if not tagged_words:
        return None, ""

    first_word, first_tag = tagged_words[0]

    if (
        first_tag == "WRB"
        and first_word == "Where"
        and len(tagged_words) > 1
        and tagged_words[1][1] == "VBN"
    ):
        return "where_was_born", extract_proper_nouns(tagged_words)
    if first_word == "How":
        return "how_to_cook", extract_proper_nouns(tagged_words)
    if first_tag == "WRB":
        return "where_is", extract_after_question_word(tagged_words)
    if first_word == "What":
        return "what_is", extract_after_question_word(tagged_words)
    if first_tag == "WP":
        return "who_is", extract_proper_nouns(tagged_words)
    return None, ""


HANDLERS = {
    "where_was_born": sparql.whereWasBorn,
    "how_to_cook": sparql.howToCook,
    "where_is": sparql.whereIs,
    "what_is": sparql.whatIs,
    "who_is": sparql.whoIs,
}


def main():
    ensure_nltk_data()

    search = input("Search: ")
    intent, term = parse_question(search)

    if intent is None:
        print("Question type not supported.")
        return

    print("Searching...")
    try:
        HANDLERS[intent](term)
    except urllib.error.HTTPError as e:
        print("DBpedia is unavailable right now (HTTP %s). Try again later." % e.code)


if __name__ == "__main__":
    main()
