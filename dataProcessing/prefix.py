from pytz import timezone
import os
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import spotlight


class PrefixGestionary :
    def __init__(self, fichier="../data/config/prefixes.json"):
        self.fichier = fichier

    def loadPrefix(self):
        try:
            with open(self.fichier, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def savePrefix(self, prefix):
        with open(self.fichier, "w") as file:
            json.dump(prefix, file, indent=4)


dictionaryLang = {
    "EN": "English",
    "FR": "French",
    "DE": "German",
    "None" : "None",
}