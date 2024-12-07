import streamlit as st
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Charger les données des tweets
with open('data/tweets/output_data.json', 'r', encoding='utf-8') as file:
    tweets_data = json.load(file)

maxLength = len(tweets_data)


def space(spaceLength):
    st.markdown(f"<div style='margin-bottom: {spaceLength}px;'></div>", unsafe_allow_html=True)


with st.sidebar:
    tweet_number = st.number_input("Numéro du Tweet à afficher", min_value=1, max_value=maxLength, step=1)

    if tweet_number > len(tweets_data):
        tweet_content = "Numéro de tweet non valide."
    else:
        tweet_content = tweets_data[f"{tweet_number - 1}"]["default"]

    # Sélectionner soit la confidence soit le support
    analysis_type = st.radio("Choisissez le type d'analyse:", ("Confidence", "Support", "General"))

# Contenu principal
st.markdown("""
    <style>
        .title-container {
            text-align: center;
            margin-bottom: 20px;
        }

    </style>
    <div class="title-container">
        <h1>Analyse des Tweets et Mots-clés</h1>
    </div>
""", unsafe_allow_html=True)
col0, col1, col00 = st.columns([1, 6, 1])
all_Element = []
if tweet_number <= len(tweets_data):
    tweet_details = tweets_data[f"{tweet_number - 1}"]["details"]
    if analysis_type == "Support":
        # we take all confidence value to let the user choose one value and display the graph of the evolution of the support
        all_Element = list(tweet_details.keys())
        all_Element = [round(float(conf), 3) for conf in all_Element]
        all_Element.sort()
        elementAnalysed = "Confidence"
    elif analysis_type == "Confidence":
        # we take all support value to let the user choose one value and display the graph of the evolution of the confidence
        all_Element = []
        for conf_details in tweet_details.values():
            all_Element.extend([int(sup) for sup in conf_details.keys()])
        all_Element = sorted(set(all_Element))
        elementAnalysed = "Support"
    else:
        # default
        all_Element = list(tweet_details.keys())
        all_Element = [round(float(conf), 3) for conf in all_Element]
        all_Element.sort()
        elementAnalysed = "General"

else:
    st.error("Numéro de tweet non valide.")


def getElementForGraph():  # selected_parameters
    analysis_counts = {}
    analysis_element = []
    keyword_counts = []
    dictionaryText = {}
    if analysis_type == "Support":
        analysis_counts = tweet_details[f"{selected_parameters}"].items()
        analysis_element = [int(sup) for sup, _ in analysis_counts]
        keyword_counts = [len(details["keywords"]) for sup, details in analysis_counts]
        dictionaryText = {"x": "Support", "y": "Nombre de mots-clés",
                          "title": f"Analyse pour Confidence = {selected_parameters}"}
    elif analysis_type == "Confidence":
        analysis_counts = {}
        for conf, conf_details in tweet_details.items():
            if f"{selected_parameters}" in conf_details:
                analysis_counts[float(conf)] = len(conf_details[f"{selected_parameters}"]["keywords"])
        analysis_element = sorted(analysis_counts.keys())
        keyword_counts = [analysis_counts[conf] for conf in analysis_element]
        dictionaryText = {"x": "Confidence", "y": "Nombre de mots-clés",
                          "title": f"Analyse pour Support = {selected_parameters}"}
    return analysis_counts, analysis_element, keyword_counts, dictionaryText


with col1:
    if analysis_type == "Support" or analysis_type == "Confidence":
        selected_parameters = st.select_slider(
            f"Sélectionnez une valeur pour la {elementAnalysed}",
            options=all_Element
        )
        analysis_counts, analysis_element, keyword_counts, dictionaryText = getElementForGraph()

        fig, ax = plt.subplots(figsize=(12, 5))  # Largeur = 8 pouces, hauteur = 5 pouces

        # Tracer les données
        ax.plot(analysis_element, keyword_counts, marker='o', color='skyblue', linestyle='-')
        ax.set_xlabel(dictionaryText["x"])
        ax.set_ylabel(dictionaryText["y"])
        ax.set_title(dictionaryText["title"])

        # Ajuster les marges pour éviter les chevauchements
        plt.tight_layout()

        # Afficher le graphique dans un conteneur limité
        st.pyplot(fig)

        # Construire et afficher le tableau
        st.markdown(f"### Détails pour chaque valeur de {dictionaryText['x']}")
        table_data = []

        if analysis_type == "Support":
            for sup, details in tweet_details[f"{selected_parameters}"].items():
                table_data.append({
                    dictionaryText["x"]: int(sup),
                    "Mots-clés": ", ".join(details["keywords"])
                })
        elif analysis_type == "Confidence":
            sorted_conf_details = sorted(tweet_details.items(), key=lambda x: float(x[0]))
            for conf, conf_details in sorted_conf_details:
                if f"{selected_parameters}" in conf_details:
                    table_data.append({
                        dictionaryText["x"]: round(float(conf), 3),
                        "Mots-clés": ", ".join(conf_details[f"{selected_parameters}"]["keywords"])
                    })

        # Afficher les données sous forme de tableau
        if table_data:
            st.table(table_data)
        else:
            st.warning("Aucune donnée à afficher pour les paramètres sélectionnés.")

    if analysis_type == "General":
        # Graphique pour la moyenne des mots-clés par Confidence
        confidence_values = []
        confidence_means = []
        for conf, conf_details in tweet_details.items():
            total_keywords = 0
            total_counts = 0
            for sup, details in conf_details.items():
                total_keywords += len(details["keywords"])
                total_counts += 1
            confidence_values.append(float(conf))
            confidence_means.append(total_keywords / total_counts if total_counts > 0 else 0)

        fig1, ax1 = plt.subplots(figsize=(12, 5))
        ax1.plot(sorted(confidence_values),
                 [confidence_means[confidence_values.index(c)] for c in sorted(confidence_values)],
                 marker='o', color='skyblue', linestyle='-')
        ax1.set_xlabel("Confidence")
        ax1.set_ylabel("Moyenne des mots-clés")
        ax1.set_title("Moyenne des mots-clés par Confidence")
        st.pyplot(fig1)

        # Graphique pour la moyenne des mots-clés par Support
        support_dict = {}
        for conf_details in tweet_details.values():
            for sup, details in conf_details.items():
                sup = int(sup)
                if sup not in support_dict:
                    support_dict[sup] = {"total_keywords": 0, "count": 0}
                support_dict[sup]["total_keywords"] += len(details["keywords"])
                support_dict[sup]["count"] += 1

        support_values = sorted(support_dict.keys())
        support_means = [support_dict[sup]["total_keywords"] / support_dict[sup]["count"] for sup in support_values]

        fig2, ax2 = plt.subplots(figsize=(12, 5))
        ax2.plot(support_values, support_means, marker='o', color='orange', linestyle='-')
        ax2.set_xlabel("Support")
        ax2.set_ylabel("Moyenne des mots-clés")
        ax2.set_title("Moyenne des mots-clés par Support")
        st.pyplot(fig2)


