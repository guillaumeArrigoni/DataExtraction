import tools as tl
import sparqlGestionary as sg
import constants as cst
import parameterElements as pe
import prefix as prefix
import annotationGestionary as ag
import json
from datasets import load_dataset
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
def display_fields():
    try:
        dernier_fichier = tl.latestFile(cst.folder_path)
        print(f"Dernier fichier trouvé : {dernier_fichier}")

        uris, surfaceForm = tl.extractURIAndSurfaceFormFromFile(dernier_fichier)

        for uri in uris:
            print(f"\nURI: {uri}")
            informations = sg.obtenir_informations(uri, pe.parameters)

            for info in informations:
                for champVar in pe.allChamps :
                    if champVar in info:
                        for champ in info[champVar]:
                            value = champ["value"]
                            if champ["lang"] in prefix.dictionaryLang:
                                lang = prefix.dictionaryLang[champ["lang"]]
                            else:
                                lang = prefix.dictionaryLang["None"]
                            print(f"{champVar}: {lang} :\n{value}\n")

    except FileNotFoundError as e:
        print(e)


def saveDataExtractedFromSparQL():
    dictionarySurfaceFormToComment = {}
    dictionarySurfaceFormToAllData = {}
    try:
        dernier_fichier = tl.latestFile(cst.folder_path)
        print(f"Dernier fichier trouvé : {dernier_fichier}")

        uris, surfaceForms = tl.extractURIAndSurfaceFormFromFile(dernier_fichier)
        for i in range(len(uris)):
            uri = uris[i]
            surfaceForm = surfaceForms[i]
            informations = sg.obtenir_informations(uri, pe.parameters) #extractFirstSentence
            for info in informations:
                for champVar in pe.allChamps :
                    if champVar in info:
                        for champ in info[champVar]:
                            value = champ["value"]
                            if champ["lang"] and champ["lang"].upper() in prefix.dictionaryLang:
                                lang = prefix.dictionaryLang[champ["lang"].upper()]
                            else:
                                lang = prefix.dictionaryLang["None"]

                            if champVar == "comment":
                                if surfaceForm not in dictionarySurfaceFormToComment:
                                    dictionarySurfaceFormToComment[surfaceForm] = {}
                                firstSentence = tl.extractFirstSentence(value)
                                dictionarySurfaceFormToComment[surfaceForm][lang] = firstSentence

                            if surfaceForm not in dictionarySurfaceFormToAllData:
                                dictionarySurfaceFormToAllData[surfaceForm] = {}

                            if lang == "None":
                                if champVar == "wikiPageExternalLink" :
                                    if champVar not in dictionarySurfaceFormToAllData[surfaceForm]:
                                        dictionarySurfaceFormToAllData[surfaceForm][champVar] = [value]
                                    else :
                                        dictionarySurfaceFormToAllData[surfaceForm][champVar].append(value)
                                else :
                                    dictionarySurfaceFormToAllData[surfaceForm][champVar] = value
                            else :
                                if champVar not in dictionarySurfaceFormToAllData[surfaceForm]:
                                    dictionarySurfaceFormToAllData[surfaceForm][champVar] = {}
                                dictionarySurfaceFormToAllData[surfaceForm][champVar][lang] = value


        with open('../data/sparql/dictionarySurfaceFormToComment.json', 'w', encoding='utf-8') as json_file:
            json.dump(dictionarySurfaceFormToComment, json_file, ensure_ascii=False, indent=4)

        with open('../data/sparql/dictionarySurfaceFormToAllData.json', 'w', encoding='utf-8') as json_file:
            json.dump(dictionarySurfaceFormToAllData, json_file, ensure_ascii=False, indent=4)
        print("Données sauvegardées dans les fichiers JSON.")
    except FileNotFoundError as e:
        print(e)

def enrich_text_with_json(json_file_path, target_string):
    """
    Cherche des mots-clés dans une chaîne cible et insère après chaque mot-clé
    la phrase associée à la clé "English" du fichier JSON.

    Args:
        json_file_path (str): Chemin vers le fichier JSON contenant les mots-clés et les descriptions.
        target_string (str): La chaîne à enrichir.

    Returns:
        str: La chaîne enrichie.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la lecture ou du traitement du fichier JSON: {e}")

    for keyword, details in data.items():
        if "English" in details:
            english_text = details["English"]
            target_string = target_string.replace(keyword, f"{keyword} {{{english_text}}} ")

    return target_string


json_file = "../data/sparql/dictionarySurfaceFormToComment.json"
output_file = "../data/tweets/output_data.json"

# Charger le dataset
dataset = load_dataset("zeroshot/twitter-financial-news-topic")

# Obtenir les premiers tweets
tweets = dataset['train']['text'][:20]

# Charger les données existantes si le fichier existe
if os.path.exists(output_file):
    with open(output_file, 'r', encoding='utf-8') as file:
        M = json.load(file)
else:
    M = {}

for i, tweet in enumerate(tweets):
    for cstConfidenceIndex in range(1, 10):
        cstConfidence = 0.1 * cstConfidenceIndex

        for cstSupport in range(5, 105, 5):
            # Vérification de l'existence des données
            if str(i) in M and str(cstConfidence) in M[str(i)]["details"] and str(cstSupport) in M[str(i)]["details"][str(cstConfidence)]:
                continue  # Passer cette itération si les données existent déjà

            name = f"tweet_{i+1}_{cstConfidenceIndex}_{cstSupport}_"

            # Créer et sauvegarder les données extraites de SparQL
            ag.createJSONUsingURI(tweet, name, cstConfidence, cstSupport)  # Implémentation requise
            saveDataExtractedFromSparQL()  # Implémentation requise

            # Enrichir le texte du tweet
            enriched_text = enrich_text_with_json(json_file, tweet)
            all_data_file = "../data/sparql/dictionarySurfaceFormToAllData.json"

            with open(all_data_file, 'r', encoding='utf-8') as file:
                all_data = json.load(file)
            keywords = all_data  # Recherche des données supplémentaires

            # Construction des détails
            if str(i) not in M:
                M[str(i)] = {"default": tweet, "details": {}}

            if str(cstConfidence) not in M[str(i)]["details"]:
                M[str(i)]["details"][str(cstConfidence)] = {}

            M[str(i)]["details"][str(cstConfidence)][str(cstSupport)] = {
                "enriched": enriched_text,
                "keywords": keywords,
            }

            # Sauvegarde dans le fichier JSON après chaque itération
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(M, file, indent=4, ensure_ascii=False)

print(f"Les données ont été sauvegardées dans {output_file}")
