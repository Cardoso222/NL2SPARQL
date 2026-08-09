import urllib.error
from unittest import mock

import pytest

import sparql


def http_error(code):
    return urllib.error.HTTPError("https://dbpedia.org/sparql", code, "err", {}, None)


def binding(**kwargs):
    return {key: {"value": value} for key, value in kwargs.items()}


class TestRunQuery:
    def make_wrapper(self, side_effects):
        wrapper = mock.MagicMock()
        results = []
        for effect in side_effects:
            if isinstance(effect, Exception):
                results.append(effect)
            else:
                query_result = mock.MagicMock()
                query_result.convert.return_value = {
                    "results": {"bindings": effect}
                }
                results.append(query_result)
        wrapper.query.side_effect = results
        return wrapper

    def test_returns_bindings(self):
        wrapper = self.make_wrapper([[binding(x="1")]])
        with mock.patch.object(sparql, "SPARQLWrapper", return_value=wrapper):
            assert sparql.run_query("SELECT 1") == [binding(x="1")]

    def test_retries_on_503(self):
        wrapper = self.make_wrapper([http_error(503), http_error(503), [binding(x="1")]])
        with mock.patch.object(sparql, "SPARQLWrapper", return_value=wrapper), \
                mock.patch.object(sparql.time, "sleep") as sleep:
            assert sparql.run_query("SELECT 1") == [binding(x="1")]
        assert wrapper.query.call_count == 3
        assert sleep.call_count == 2

    def test_raises_after_exhausting_retries(self):
        wrapper = self.make_wrapper([http_error(503)] * 5)
        with mock.patch.object(sparql, "SPARQLWrapper", return_value=wrapper), \
                mock.patch.object(sparql.time, "sleep"):
            with pytest.raises(urllib.error.HTTPError):
                sparql.run_query("SELECT 1", retries=5)
        assert wrapper.query.call_count == 5

    def test_non_503_not_retried(self):
        wrapper = self.make_wrapper([http_error(400)])
        with mock.patch.object(sparql, "SPARQLWrapper", return_value=wrapper):
            with pytest.raises(urllib.error.HTTPError):
                sparql.run_query("SELECT 1")
        assert wrapper.query.call_count == 1


class TestGetDescription:
    def test_returns_portuguese_first(self):
        with mock.patch.object(
            sparql, "run_query", return_value=[binding(description="descrição pt")]
        ) as run:
            assert sparql.get_description("Bitcoin") == "descrição pt"
        assert run.call_count == 1
        assert "LANG(?description) = 'pt'" in run.call_args[0][0]

    def test_falls_back_to_english(self):
        with mock.patch.object(
            sparql,
            "run_query",
            side_effect=[[], [binding(description="english description")]],
        ) as run:
            assert sparql.get_description("Bitcoin") == "english description"
        assert run.call_count == 2
        assert "LANG(?description) = 'en'" in run.call_args[0][0]

    def test_returns_none_when_nothing_found(self):
        with mock.patch.object(sparql, "run_query", return_value=[]):
            assert sparql.get_description("Nonexistent") is None

    def test_type_constraint_is_injected(self):
        with mock.patch.object(
            sparql, "run_query", return_value=[binding(description="x")]
        ) as run:
            sparql.get_description("Someone", "?thing rdf:type dbo:Person.")
        assert "?thing rdf:type dbo:Person." in run.call_args[0][0]


class TestHandlers:
    def test_who_is_prints_description(self, capsys):
        with mock.patch.object(sparql, "get_description", return_value="um músico"):
            sparql.whoIs("Caetano Veloso")
        assert capsys.readouterr().out.strip() == "um músico"

    def test_who_is_prints_not_found(self, capsys):
        with mock.patch.object(sparql, "get_description", return_value=None):
            sparql.whoIs("Nonexistent Person")
        assert "No results found" in capsys.readouterr().out

    def test_what_is_prints_description(self, capsys):
        with mock.patch.object(sparql, "get_description", return_value="moeda digital"):
            sparql.whatIs("Bitcoin")
        assert capsys.readouterr().out.strip() == "moeda digital"

    def test_where_is_prints_all_places(self, capsys):
        results = [binding(placeLabel="Lambeth"), binding(placeLabel="London")]
        with mock.patch.object(sparql, "run_query", return_value=results):
            sparql.whereIs("London Eye")
        assert capsys.readouterr().out.splitlines() == ["Lambeth", "London"]

    def test_where_is_prints_not_found(self, capsys):
        with mock.patch.object(sparql, "run_query", return_value=[]):
            sparql.whereIs("Nowhere")
        assert "No results found" in capsys.readouterr().out

    def test_where_was_born_prints_places(self, capsys):
        results = [binding(birthPlace="Brazil"), binding(birthPlace="Santo Amaro, Bahia")]
        with mock.patch.object(sparql, "run_query", return_value=results):
            sparql.whereWasBorn("Caetano Veloso")
        assert capsys.readouterr().out.splitlines() == ["Brazil", "Santo Amaro, Bahia"]

    def test_how_to_cook_prints_description_and_ingredients(self, capsys):
        results = [binding(description="Doce típico", ingredients="leite, chocolate")]
        with mock.patch.object(sparql, "run_query", return_value=results):
            sparql.howToCook("Brigadeiro")
        out = capsys.readouterr().out
        assert "Doce típico" in out
        assert "Ingredientes: leite, chocolate" in out

    def test_how_to_cook_handles_missing_optional_fields(self, capsys):
        with mock.patch.object(sparql, "run_query", return_value=[{}]):
            sparql.howToCook("Mystery Dish")
        assert capsys.readouterr().out == ""

    def test_how_to_cook_prints_not_found(self, capsys):
        with mock.patch.object(sparql, "run_query", return_value=[]):
            sparql.howToCook("Nonexistent Dish")
        assert "No results found" in capsys.readouterr().out
