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


def whereis(location):
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
  sql = """ 
      PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
      PREFIX dbo: <http://dbpedia.org/ontology/>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

      SELECT *
      WHERE  { 
        ?location a dbo:Location .
        ?location dbo:location ?country.
        ?location rdfs:label ?label.
        ?country rdfs:label ?countryLabel.
        
        FILTER regex(?label, "^%s", "i").
        OPTIONAL {
          FILTER (lang(?countryLabel) = 'pt')
        }


      }
      LIMIT 1
      """ % ''.join((location))

  sparql.setQuery(sql)
  

  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()

  for result in results["results"]["bindings"]:
      print(result["countryLabel"]["value"])


def whatis(term):
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
  sql = """ 
  PREFIX w3-owl: <http://www.w3.org/2002/07/owl#>
  SELECT ?thing, ?comment, ?label
    WHERE {
      ?thing rdf:type w3-owl:Thing.
      ?thing rdfs:comment ?comment.
      ?thing rdfs:label ?label.
      FILTER regex(?label, "^%s", "i").
      FILTER (lang(?comment) = 'pt')
    }
  LIMIT 1
  """ % ''.join((term))

  sparql.setQuery(sql)

  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()

  for result in results["results"]["bindings"]:
      print(result["comment"]["value"])

def howtocook(term):
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
  sql = """ 
  PREFIX  dbpedia-owl:  <http://dbpedia.org/ontology/>
  PREFIX dbpedia: <http://dbpedia.org/resource>
  PREFIX dbpprop: <http://dbpedia.org/property>
     SELECT *
      WHERE {
        ?dessert rdf:type dbpedia-owl:Food.
        ?dessert dbpedia-owl:ingredientName ?ing.
        ?dessert dbpedia-owl:servingTemperature ?servingTemp.
        ?dessert rdfs:comment ?comment.
        ?dessert rdfs:label ?label.
        FILTER regex(?label, "^%s", "i")
        
        FILTER (LANG(?comment) = 'pt') 

      }
      LIMIT 1
  """ % ''.join((term))

  sparql.setQuery(sql)

  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()

  for result in results["results"]["bindings"]:
      print(result["comment"]["value"] + "\n")
      print('Ingredientes: ' + result["ing"]["value"] + "\n")
      print('Servir: ' + result["servingTemp"]["value"] + "\n")