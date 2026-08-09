import main


class TestParseQuestion:
    def test_where_was_born(self):
        intent, term = main.parse_question("Where was born Caetano Veloso?")
        assert intent == "where_was_born"
        assert term == "Caetano Veloso"

    def test_who_is(self):
        intent, term = main.parse_question("Who is Caetano Veloso?")
        assert intent == "who_is"
        assert term == "Caetano Veloso"

    def test_where_is(self):
        intent, term = main.parse_question("Where is London Eye?")
        assert intent == "where_is"
        assert term == "London Eye"

    def test_what_is(self):
        intent, term = main.parse_question("What is Bitcoin?")
        assert intent == "what_is"
        assert term == "Bitcoin"

    def test_how_to_cook(self):
        intent, term = main.parse_question("How to cook Brigadeiro?")
        assert intent == "how_to_cook"
        assert term == "Brigadeiro"

    def test_empty_input(self):
        intent, term = main.parse_question("")
        assert intent is None
        assert term == ""

    def test_only_stopwords(self):
        intent, term = main.parse_question("is the a an")
        assert intent is None

    def test_unsupported_question(self):
        intent, term = main.parse_question("Bananas everywhere yesterday")
        assert intent is None


class TestExtractors:
    def test_extract_proper_nouns_joins_with_spaces(self):
        tagged = [("Where", "WRB"), ("Caetano", "NNP"), ("Veloso", "NNP")]
        assert main.extract_proper_nouns(tagged) == "Caetano Veloso"

    def test_extract_proper_nouns_ignores_other_tags(self):
        tagged = [("cook", "VB"), ("Brigadeiro", "NNP")]
        assert main.extract_proper_nouns(tagged) == "Brigadeiro"

    def test_extract_after_question_word_drops_wh_and_punctuation(self):
        tagged = [("What", "WP"), ("Bitcoin", "NNP"), ("?", ".")]
        assert main.extract_after_question_word(tagged) == "Bitcoin"

    def test_extract_after_question_word_keeps_multiword_terms(self):
        tagged = [("Where", "WRB"), ("London", "NNP"), ("Eye", "NNP"), ("?", ".")]
        assert main.extract_after_question_word(tagged) == "London Eye"


class TestHandlers:
    def test_every_intent_has_a_handler(self):
        assert set(main.HANDLERS) == {
            "where_was_born",
            "how_to_cook",
            "where_is",
            "what_is",
            "who_is",
        }
