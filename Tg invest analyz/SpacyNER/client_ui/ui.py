import json
import re

import requests
import streamlit as st

URL_DEFAULT = "http://....:8560/recognize"
NEWS_DEFAULT = "Роснефть: топ-выбор в нефтянке на 2023 Рекомендация — Покупать"
LABEL_COLORS = {
    "ORG": "#AFEEEE",
    "TICKER": "#7FFFD4",
    "ACT": "#40E0D0",
    "PERCENT": "#48D1CC",
    "PRICE": "#00CED1",
    "TIME": "#5F9EA0",
}


def get_response(URL: str, NEWS: str) -> str:
    resp = requests.post(URL, json={"text": NEWS})
    resp_text = resp.text
    return resp_text


def find_entities(resp: str, news: str) -> str:
    resp = json.loads(resp)
    for entity in resp:
        class_name, text = list(entity.items())[0]
        color = LABEL_COLORS[class_name]
        text = text.strip()
        news = re.sub(rf"[^>]{text}", f' <span style="background-color: {color}">{text} [{class_name}]</span>', news)
    news = "<p>" + news + "</p>"
    return news


URL = st.text_input("Введите URL сервиса", value=URL_DEFAULT)

col1, col2 = st.columns(2)
with col1:
    NEWS = st.text_area("Введите текст инвестиционной идеи", value=NEWS_DEFAULT, height=250)
    #  Почему-то не распознает первое слово.
    #  Если добавить пробел на стороне сервиса, ничего не меняется. Нужно доучить
    NEWS = " " + NEWS
    button = st.button("Распознать")

with col2:
    st.markdown("**Распознанный текст**")
    if button:
        resp = get_response(URL, NEWS)
        text = find_entities(resp, NEWS)
        st.markdown(text, unsafe_allow_html=True)
        st.stop()
