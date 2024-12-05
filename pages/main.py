import streamlit as st

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from gestionary.navigation import get_nav_from_toml


st.set_page_config(layout="wide")

# Ajustement du padding global
st.markdown("""
    <style>
    .main {
        padding: 0 !important; /* Supprime les padding inutiles globaux */
    }
    .block-container {
        padding: 50px 0px 50px 0px !important; /* 50px de padding vertical, 20px pour les marges horizontales */
    }
    </style>
    """, unsafe_allow_html=True)


nav = get_nav_from_toml(
    "pages/.streamlit/pages.toml"
)
print(nav)
pg = st.navigation(nav)

pg.run()