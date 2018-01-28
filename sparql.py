from SPARQLWrapper import SPARQLWrapper, JSON


def whois(person):
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
  sql = """ 
      PREFIX  dbpedia-owl:  <http://dbpedia.org/ontology/>
      PREFIX dbpedia: <http://dbpedia.org/resource>
      PREFIX dbpprop: <http://dbpedia.org/property>

     SELECT DISTINCT ?person ?comment ?label
      WHERE {
        ?person rdf:type dbpedia-owl:Person.
        ?person rdfs:comment ?comment.  
        ?person rdfs:label ?label
        FILTER regex(?label, "^%s", "i")
        FILTER (LANG(?comment) = 'pt') 
      }
      LIMIT 1
      """ % ''.join((person))

  sparql.setQuery(sql)
  

  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()

  for result in results["results"]["bindings"]:
      print(result["comment"]["value"])
