import json
import spotlight
import tools as tl
import constants as cst

def createJSONUsingURI(text, fileNameTag : str = "", confidence : float = cst.confidence, support : int = cst.support) :
    if not tl.isValidFileName(fileNameTag):
        print("Le nom du fichier contient des caractères invalides")
        return
    file_name = 'annotations_' + fileNameTag + tl.currentTime() + '.json'
    output_file = cst.folder_path + '/' + file_name

    try:
        annotations = spotlight.annotate(
            cst.spotlight_url,
            text,
            confidence=confidence,
            support=support
        )

        with open(output_file, 'w') as f:
            json.dump(annotations, f, indent=4)

        print(f"Annotations sauvegardées dans {output_file}")
    except spotlight.SpotlightException as e:
        print(f"Erreur lors de l'annotation : {e}")