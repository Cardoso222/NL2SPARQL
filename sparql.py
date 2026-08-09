import time
import urllib.error

from SPARQLWrapper import SPARQLWrapper, JSON

ENDPOINT = "https://dbpedia.org/sparql"
USER_AGENT = "NL2SPARQL/1.0 (https://github.com/Cardoso222/NL2SPARQL)"

PREFIXES = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""


def run_query(query, retries=5):
    # DBpedia's public endpoint rate-limits aggressively (intermittent 503s)
    sparql = SPARQLWrapper(ENDPOINT, agent=USER_AGENT)
    sparql.setQuery(PREFIXES + query)
    sparql.setReturnFormat(JSON)
    for attempt in range(retries):
        try:
            return sparql.query().convert()["results"]["bindings"]
        except urllib.error.HTTPError as e:
            if e.code == 503 and attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
            else:
                raise
    return []


def get_description(term, type_constraint=""):
    # dbo:description replaced rdfs:comment/dbo:abstract in current DBpedia
    # snapshots; prefer Portuguese, fall back to English
    for lang in ("pt", "en"):
        query = """
            SELECT DISTINCT ?description
            WHERE {
              ?thing rdfs:label "%s"@en.
              %s
              ?thing dbo:description ?description.
              FILTER (LANG(?description) = '%s')
            }
            LIMIT 1
        """ % (term, type_constraint, lang)
        results = run_query(query)
        if results:
            return results[0]["description"]["value"]
    return None


def whoIs(person):
    description = get_description(person, "?thing rdf:type dbo:Person.")
    if description:
        print(description)
    else:
        print("No results found for '%s'." % person)


def whatIs(term):
    description = get_description(term)
    if description:
        print(description)
    else:
        print("No results found for '%s'." % term)


def whereIs(location):
    query = """
        SELECT DISTINCT ?placeLabel
        WHERE {
          ?location rdfs:label "%s"@en.
          ?location dbo:location ?place.
          ?place rdfs:label ?placeLabel.
          FILTER (LANG(?placeLabel) = 'en')
        }
        LIMIT 3
    """ % location
    results = run_query(query)
    if not results:
        print("No results found for '%s'." % location)
    for result in results:
        print(result["placeLabel"]["value"])


def whereWasBorn(person):
    query = """
        SELECT DISTINCT ?birthPlace
        WHERE {
          ?person rdf:type dbo:Person.
          ?person rdfs:label "%s"@en.
          ?person dbo:birthPlace ?place.
          ?place rdfs:label ?birthPlace.
          FILTER (LANG(?birthPlace) = 'en')
        }
        LIMIT 3
    """ % person
    results = run_query(query)
    if not results:
        print("No results found for '%s'." % person)
    for result in results:
        print(result["birthPlace"]["value"])


def howToCook(term):
    query = """
        SELECT DISTINCT ?description ?ingredients
        WHERE {
          ?food rdf:type dbo:Food.
          ?food rdfs:label "%s"@en.
          OPTIONAL {
            ?food dbo:description ?description.
            FILTER (LANG(?description) = 'pt')
          }
          OPTIONAL { ?food dbo:ingredientName ?ingredients }
        }
        LIMIT 1
    """ % term
    results = run_query(query)
    if not results:
        print("No results found for '%s'." % term)
    for result in results:
        if "description" in result:
            print(result["description"]["value"] + "\n")
        if "ingredients" in result:
            print("Ingredientes: " + result["ingredients"]["value"])
