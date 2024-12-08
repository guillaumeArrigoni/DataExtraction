import streamlit as st
import re
import os

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

IMAGE_DIR = "rapport"
def st_markdown(markdown_string):
    title = ""
    parts = re.split(r"!\[(.*?)\]\((.*?)\)", markdown_string)
    for i, part in enumerate(parts):
        if i % 3 == 0:
            st.markdown(part)
        elif i % 3 == 1:
            title = part
        else:
            image_path = os.path.join(IMAGE_DIR, part)
            if title == "" or title.lower() == "alt text":
                st.image(image_path)
            else :
                st.image(image_path, caption=title)


with col1:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()
        st_markdown(markdown_content)
    except FileNotFoundError:
        st.error(f"Le fichier Markdown spécifié n'a pas été trouvé : {file_path}")


