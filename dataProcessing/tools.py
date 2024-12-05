import json
from pytz import timezone
import os
from datetime import datetime
import re


def latestFile(dossier):
    try:
        fichiers = [os.path.join(dossier, f) for f in os.listdir(dossier) if f.endswith('.json')]
        dernier_fichier = max(fichiers, key=os.path.getctime)
        return dernier_fichier
    except ValueError:
        raise FileNotFoundError("Aucun fichier JSON trouvé dans le dossier.")

def currentTime(timeZoneVar : str = "Europe/Paris"):
    format = "%Y-%m-%d_%Hh%Mm%Ss"
    now_utc = datetime.now(timezone('UTC'))
    local_tz = timezone(timeZoneVar)
    now_local = now_utc.astimezone(local_tz)
    return now_local.strftime(format)

def extractURIAndSurfaceFormFromFile(fichier):
    with open(fichier, 'r') as f:
        annotations = json.load(f)
    uris = []
    surfaceForm = []
    for annotation in annotations:
        if 'URI' in annotation:
            uris.append(annotation['URI'])
        if 'surfaceForm' in annotation:
            surfaceForm.append(annotation['surfaceForm'])
    return uris, surfaceForm

def isValidFileName(fileName : str) -> bool:
    return not any(c in fileName for c in ['\\', '/', ':', '*', '?', '"', '<', '>', '|'])

def extractFirstSentence(texte):
    """
    Extrait la première phrase d'un texte.

    Args:
        texte (str): Le texte d'entrée.

    Returns:
        str: La première phrase extraite.
    """
    # Expression régulière pour capturer la première phrase.
    # On considère une phrase comme se terminant par '.', '!', ou '?'.
    match = re.match(r'(.*?[.!?])(\s*[A-Z]|$)', texte)
    if match:
        return match.group(1)
    else:
        return texte