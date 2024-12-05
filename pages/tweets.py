import streamlit as st
import json

with open('data/tweets/output_data.json', 'r', encoding='utf-8') as file:
    tweets_data = json.load(file)
maxLength = len(tweets_data)
def space(spaceLength) :
    st.markdown(f"<div style='margin-bottom: {spaceLength}px;'></div>", unsafe_allow_html=True)

with st.sidebar:
    tweet_number = st.number_input("Numéro du Tweet à afficher", min_value=1, max_value=maxLength, step=1)

    if tweet_number > len(tweets_data):
        tweet_content = "Numéro de tweet non valide."
    else :
        tweet_content = tweets_data[f"{tweet_number-1}"]["default"]

    # Sélectionner un mot à analyser parmi les mots-clés
    if len(tweets_data[f"{tweet_number-1}"]["details"]) > 1 :
        valConfidence = list(tweets_data[f"{tweet_number-1}"]["details"].keys())
        for i in range(0, len(valConfidence)) :
            valConfidence[i] = float(valConfidence[i])
        valConfidence.sort()

        slider_value_confidence = st.select_slider(
            "Sélectionnez une valeur pour la confidence",
            options=valConfidence
        )
    else :
        slider_value_confidence = list(tweets_data[f"{tweet_number-1}"]["details"].keys())[0]

    if len(tweets_data[f"{tweet_number-1}"]["details"][f"{slider_value_confidence}"]) > 1 :
        valSupport = list(tweets_data[f"{tweet_number - 1}"]["details"][f"{slider_value_confidence}"].keys())
        for i in range(0, len(valSupport)):
            valSupport[i] = int(valSupport[i])
        valSupport.sort()
        slider_value_support = int(st.select_slider(
            "Sélectionnez une valeur pour le support",
            options=valSupport
        ))
    else :
        slider_value_support = list(tweets_data[f"{tweet_number-1}"]["details"][f"{slider_value_confidence}"].keys())[0]

    words = list(tweets_data[f"{tweet_number-1}"]["details"][f"{slider_value_confidence}"][f"{slider_value_support}"]["keywords"].keys())
    selected_word = st.selectbox("Sélectionnez un mot à analyser", words if words else ["Aucun mot disponible"])


st.markdown("""
    <style>
        .title-container {
            text-align: center;
            margin-bottom: 20px;
        }
    
        .stHorizontalBlock {
            gap: 1rem !important;  /* Enlève l'espace entre les colonnes */
            margin: 1rem !important;
        }
    </style>
    <div class="title-container">
        <h1>Analyse des Tweets et Mots-clés</h1>
    </div>
""", unsafe_allow_html=True)

# Mise en page principale : deux colonnes
col1, col2 = st.columns([1, 1])  # Colonnes de largeur égale


with col1:
    st.markdown("""<style>
                    
    
                    .stColumn:nth-child(1) {
                        background-color: rgba(144, 238, 144, 0.3); /* Vert clair semi-transparent */
                        padding: 15px;
                        border-radius: 10px;
                        text-align: center;  /* Centrage horizontal */
                        display: flex;
                        flex-direction: column;
                    }
                    </style>""", unsafe_allow_html=True)
    st.subheader("Tweet sélectionné")
    st.write(tweet_content)
    space(50)
    st.subheader("Texte enrichi")
    enriched_text = tweets_data[f"{tweet_number-1}"]["details"][f"{slider_value_confidence}"][f"{slider_value_support}"]["enriched"]
    st.write(enriched_text)

with col2:
    st.markdown("""<style>   
                    .stColumn:nth-child(2) {
                        background-color: rgba(173, 216, 230, 0.3);  /* Bleu clair semi-transparent */
                        padding: 15px;
                        border-radius: 10px;
                        text-align: center;  /* Centrage horizontal */
                        display: flex;
                        flex-direction: column;
                    }
                    
                    .image-container {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        margin: 10px 0;
                    }
                    
                    .image-container img {
                        max-width: 200px; /* Limite la largeur à 200px */
                        max-height: 200px; /* Limite la hauteur à 200px */
                        border-radius: 10px; /* Ajoute des coins arrondis */
                    }
                    </style>""", unsafe_allow_html=True)

    st.subheader(f"Analyse du mot sélectionné : **{selected_word}**")
    if selected_word:
        word_details = tweets_data[f"{tweet_number-1}"]["details"][f"{slider_value_confidence}"][f"{slider_value_support}"]["keywords"].get(selected_word)

        if word_details:

            # Vérification et affichage de chaque champ
            if "thumbnail" in word_details:
                space(50)
                st.markdown(
                    f"""
                                    <div class="image-container">
                                        <img src="{word_details['thumbnail']}" alt="{selected_word}">
                                    </div>
                                    """, unsafe_allow_html=True
                )
                space(50)

            if "foundingDate" in word_details:
                st.write(f"**Date de Fondation** : {word_details['foundingDate']}")

            if "birthPlace" in word_details:
                st.write(f"**Lieu de Naissance** : {word_details['birthPlace']}")

            if "deathPlace" in word_details:
                st.write(f"**Lieu de Décès** : {word_details['deathPlace']}")

            if "country" in word_details:
                st.write(f"**Pays** : {word_details['country']}")

            if "flag" in word_details:
                st.write(f"**Drapeau** : {word_details['flag']}")

            if "region" in word_details:
                st.write(f"**Région** : {word_details['region']}")

            if "areaCode" in word_details:
                st.write(f"**Code de Zone** : {word_details['areaCode']}")

            if "leader" in word_details:
                st.write(f"**Leader** : {word_details['leader']}")

            if "officialLanguage" in word_details:
                st.write(f"**Langue Officielle** : {word_details['officialLanguage']}")

            if "languagesSpoken" in word_details:
                st.write(f"**Langues Parlées** : {word_details['languagesSpoken']}")

            if "capital" in word_details:
                st.write(f"**Capitale** : {word_details['capital']}")

            if "currency" in word_details:
                st.write(f"**Monnaie** : {word_details['currency']}")

            if "population" in word_details:
                st.write(f"**Population** : {word_details['population']}")

            if "areaTotal" in word_details:
                st.write(f"**Surface Totale** : {word_details['areaTotal']} km²")

            if "density" in word_details:
                st.write(f"**Densité** : {word_details['density']} habitants/km²")

            if "comment" in word_details:
                st.divider()
                escaped_description = word_details["comment"].get("English", "").replace('$', '&#36;')
                st.write(f"**Description** : {escaped_description}")

            if "abstract" in word_details:
                escaped_abstract = word_details["abstract"].get("English", "").replace('$', '&#36;')
                st.write(f"**Résumé** : {escaped_abstract}")

            if "wikiPageExternalLink" in word_details:
                st.divider()
                st.write(f"**Liens Externes** :")
                for link in word_details["wikiPageExternalLink"]:
                    st.markdown(f"[Plus d'infos sur l'entité : {link}]({link})")

