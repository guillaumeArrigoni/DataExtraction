from __future__ import annotations

from pathlib import Path

import streamlit as st
import toml
from streamlit.navigation.page import StreamlitPage
from streamlit.runtime.metrics_util import gather_metrics

class Page:
    path: str
    name: str | None = None
    icon: str | None = None
    url_path: str | None = None

    def __init__(self, path: str, name: str | None = None, icon: str | None = None, url_path: str | None = None):
        self.path = path
        self.name = name
        self.icon = icon
        self.url_path = url_path

    def __repr__(self):
        return f"Page(path={self.path}, name={self.name}, icon={self.icon}, url_path={self.url_path})"

    def __str__(self):
        return self.name or self.path

    def __eq__(self, other):
        return self.path == other.path


def _get_pages_from_config(
        path: str = "td2_streamlitv2/pages/.streamlit/pages.toml") -> list[Page] | None:
    """
    Given a path to a TOML file, read the file and return a list of Page objects
    """
    try:
        raw_pages: list[dict[str, str]] = toml.loads(
            Path(path).read_text(encoding="utf-8")
        )["pages"]
    except (FileNotFoundError, toml.decoder.TomlDecodeError, KeyError):
        st.error(
            f"""
        Error msg
            """
        )
        return None

    pages: list[Page] = []
    print("raw pages", raw_pages)
    for page in raw_pages:
        pages.append(Page(**page))
    return pages



def _get_nav_from_toml(
    path: str = ".streamlit/pages.toml") -> list[StreamlitPage] | dict[str, list[StreamlitPage]]:
    """
    Given a path to a TOML file, return a list or dictionary that can be passed to
    st.navigation
    """
    pages = _get_pages_from_config(path)
    if pages is None:
        return []

    pages_data = []

    for page in pages:
        pages_data.append(
            st.Page(
                page.path,
                title=page.name,
                icon=page.icon,
                url_path=page.url_path,
            )
        )

    return pages_data

get_nav_from_toml = gather_metrics("st_pages.get_nav_from_toml", _get_nav_from_toml)