import parameters as PAR


param_comment = PAR.Parameter(
    champ="comment",
    prefix="rdfs",
    prefix_url="<http://www.w3.org/2000/01/rdf-schema#>",
    filtre_langues=True,
    langues=["EN"]
)

param_abstract = PAR.Parameter(
    champ="abstract",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=True,
    langues=["EN"]
)

param_population = PAR.Parameter(
    champ="population",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=False
)

param_areaTotal = PAR.Parameter(
    champ="areaTotal",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=False
)

param_capital = PAR.Parameter(
    champ="capital",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=True,
    langues=["EN"]
)

param_leader = PAR.Parameter(
    champ="leader",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=True,
    langues=["EN"]
)

param_country = PAR.Parameter(
    champ="country",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=False
)

param_officialLanguage = PAR.Parameter(
    champ="officialLanguage",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=True,
    langues=["EN"]
)

param_areaCode = PAR.Parameter(
    champ="areaCode",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=False
)

param_thumbnail = PAR.Parameter(
    champ="thumbnail",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=False
)

param_region = PAR.Parameter(
    champ="region",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=False
)

param_currency = PAR.Parameter(
    champ="currency",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=False
)

param_flag = PAR.Parameter(
    champ="flag",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=False
)

param_foundingDate = PAR.Parameter(
    champ="foundingDate",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=False
)

param_birthPlace = PAR.Parameter(
    champ="birthPlace",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=True,
    langues=["EN"]
)

param_deathPlace = PAR.Parameter(
    champ="deathPlace",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=True,
    langues=["EN"]
)

param_languagesSpoken = PAR.Parameter(
    champ="languagesSpoken",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=True,
    langues=["EN"]
)

param_density = PAR.Parameter(
    champ="density",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=False
)

param_wikiPageExternalLink = PAR.Parameter(
    champ="wikiPageExternalLink",
    prefix="dbo",
    prefix_url="<http://dbpedia.org/ontology/>",
    filtre_langues=False
)

parameters = [
    param_comment,
    param_abstract,
    param_population,
    param_areaTotal,
    param_capital,
    param_leader,
    param_country,
    param_officialLanguage,
    param_areaCode,
    param_thumbnail,
    param_region,
    param_currency,
    param_flag,
    param_foundingDate,
    param_birthPlace,
    param_deathPlace,
    param_languagesSpoken,
    param_density,
    param_wikiPageExternalLink
]

allChamps = [param.get_champ() for param in parameters]
allFieldsWithoutLang = [param.get_champ() for param in parameters if param.filtre_langues == False]
