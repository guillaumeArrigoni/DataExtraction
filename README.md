# Fonctionnement

Ce projet a pour objectif principal de réaliser de la reconnaissance d'entités nommées (NER) pour extraire des éléments importants d'une phrase, tels que des noms comme *Tesla*. À partir de ces mots extraits, l'objectif est d'afficher diverses informations les concernant.  

Un second objectif est d'analyser l'impact des paramètres **confidence** et **support** sur l'extraction des mots, afin de mieux comprendre leur influence sur les résultats.  

## Structure du projet  

Le projet est divisé en deux parties principales :  

### 1. Extraction des entités et stockage des résultats  

#### Étapes :  
1. **Récupération des textes** :  
   Les textes utilisés pour le NER sont obtenus à partir du dataset suivant :  
   ```python
   dataset = load_dataset("zeroshot/twitter-financial-news-topic")
    ```

2. **Extraction des entités** :  
   - On utilise **Spotlight** et **SPARQL** pour identifier les entités importantes et obtenir des détails spécifiques à leur sujet.  
   - Les résultats sont stockés dans un fichier `output_data.json` qui peut être trouvé ici :  
     `/data/tweets/output_data.json`.  

#### Organisation des fichiers :  
- **Fichiers intermédiaires** :  
  - Pour éviter toute perte en cas d'échec d'une étape, des fichiers intermédiaires sont stockés :  
    - Dossier **`data/spotlight`** : détails de l'extraction des mots-clés.  
    - Dossier **`data/sparkql`** : détails des mots extraits avec SPARQL.  
    - Dossier **`data/config`** : configurations pour SPARQL, sauvegardant les derniers paramètres utilisés si l'utilisateur oublie de les préciser.  
- **Scripts associés** :  
  - Tous les scripts Python nécessaires pour cette partie sont dans le dossier `dataProcessing`.  
  - Pour lancer l'extraction, exécutez :  
    ```bash
    python dataProcessing/dataProcessing.py
    ```  

### 2. Visualisation et analyse avec Streamlit  

Cette partie du projet permet de visualiser les résultats de l'extraction et d'analyser les données.  

#### Organisation des fichiers :  
- **Pages Streamlit** :  
  - Les différentes pages du site sont situées dans le dossier `pages`.  
  - Le fichier de lancement est `pages/main.py`. Pour le lancer, exécutez la commande :  
    ```bash
    streamlit run pages/main.py
    ```
  - Le fichier `pages/.streamlit/pages.toml` contient la description des pages et leur configuration pour le menu de navigation.  
- **Navigation** :  
  - La logique de navigation est définie dans `gestionary/navigation.py`.  

#### Rapport :  
Un rapport détaillé sur le travail réalisé est disponible dans le dossier `rapport`.  

### Requirements

L'ensemble des requirements nécessaires pour faire fonctionner le projet sont présents dans le fichier `requirements.txt`.  
Pour installer l'ensemble des dépendances, il suffit d'exécuter la commande suivante :  
```bash
pip install -r requirements.txt
```

## Auteurs  

Ce projet a été réalisé par :  
- **Timothée JUILLET**  
- **Guillaume ARRIGONI**

