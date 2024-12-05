from SPARQLWrapper import JSON
import constants as cst

def obtenir_informations(uri, parameters):
    informations = []

    for param in parameters:
        champ = param.get_champ()
        prefix = param.get_prefix()
        prefix_url = param.get_prefix_url()
        doesLang, bind, filtre_langue_query, queryLang = param.get_filtre_langue_query()

        query = f"""
        PREFIX {prefix}: {prefix_url}
        SELECT ?{champ} {queryLang}
        WHERE {{
            <{uri}> {prefix}:{champ} ?{champ} .
            {bind}
            {filtre_langue_query}
        }}
        """

        cst.sparql.setQuery(query)
        cst.sparql.setReturnFormat(JSON)
        try:
            results = cst.sparql.query().convert()
            if results["results"]["bindings"]:
                champ_list = []
                for result in results["results"]["bindings"]:
                    value = result[champ]['value']
                    if len(result) > 1:
                        lang = result['lang']['value']
                    else :
                        lang = None
                    champ_list.append({"value": value, "lang": lang})
                informations.append({champ: champ_list})
        except Exception as e:
            print(f"Erreur lors de la requête SPARQL pour le champ {champ} : {e}")

    return informations