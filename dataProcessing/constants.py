from SPARQLWrapper import SPARQLWrapper

folder_path = '../data/spotlight'
spotlight_url = 'https://api.dbpedia-spotlight.org/en/annotate'
confidence = 0.4
support = 20
sparql = SPARQLWrapper("http://dbpedia.org/sparql")