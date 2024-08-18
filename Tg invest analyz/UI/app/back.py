import pandas as pd
import streamlit as st


def select_items_sidebar(items: list, label: str) -> list:
    with st.sidebar:
        selected_items = st.multiselect(label=label, options=sorted(items), default=[])
    if not selected_items:
        return sorted(items)
    return selected_items


def empty_check(df: pd.DataFrame) -> None:
    if df.empty:
        st.text("По выбранным каналам нет идей для анализа")
        st.stop()
