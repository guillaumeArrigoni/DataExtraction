import streamlit as st

file_path = "rapport/Rapport.md"

st.markdown("""
    <style>
        .title-container {
            text-align: center;
            margin-bottom: 20px;
        }

    </style>
    <div class="title-container">
        <h1>Rapport</h1>
    </div>
""", unsafe_allow_html=True)
col0, col1, col00 = st.columns([1, 6, 1])

with col1:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()
        st.markdown(markdown_content, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Le fichier Markdown spécifié n'a pas été trouvé : {file_path}")
