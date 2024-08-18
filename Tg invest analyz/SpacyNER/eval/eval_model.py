import json

import pandas as pd
import spacy
from spacy.scorer import Scorer
from spacy.tokens import Span
from spacy.training import Example

EXCEL_PATH = "test_dataset/eval_data.xlsx"
MODEL_PATH = "models/model-best"
ETHALONS_PATH = "test_dataset/ethalons.json"
SCORES_PATH = "test_dataset/scores.json"
METRICS_PATH = "metrics/metrics.json"

DICT_TEMPLATE = {
    "ORG_f": [],
    "TICKER_f": [],
    "TIME_f": [],
    "PRICE_f": [],
    "PERCENT_f": [],
    "ACT_f": [],
}

def save_json(path: str, object_name) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(object_name, file, ensure_ascii=False)


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as file:
        obj = json.load(file)
    return obj


def count_scores(ethalons: list) -> list:
    """
    Из размеченных (и исправленных данных) создает 2 дока
        1) размеченный новой моделью
        2) с сохраненной (Эталонной разметкой)
    Вычисляет метрики по каждой сущности
    """
    nlp = spacy.load(MODEL_PATH)
    scores = []
    scorer = Scorer()
    for text, ents, _ in ethalons:
        # Получаем ответ текущей модели
        pred_doc = nlp(text)

        # Создаем doc с эталонными ответами
        gold_doc = pred_doc.copy()
        span_list = [Span(gold_doc, *items) for items in ents["entities"]]
        gold_doc.set_ents(span_list)

        # Добавляем в список результатов
        scores.append(scorer.score([Example(pred_doc, gold_doc)])["ents_per_type"])
    return scores


def make_scores_series(scores: list, dict_templte: dict) -> pd.Series:
    """Создает pd.Series с результатами f-меры по каждой сущности
    ORG_f        0.953333
    TICKER_f     0.813953
    TIME_f       0.953333
    PRICE_f      0.693694
    PERCENT_f    0.900000
    ACT_f        0.800000
    """
    for score in scores:
        for key in dict_templte.keys():
            label, metrics = key.split("_")
            try:
                dict_templte[key].append(score[label][metrics])
            except Exception:
                dict_templte[key].append(None)
    scores = pd.DataFrame(dict_templte).describe().loc["mean", :]
    return scores


def append_metrics(new_metrics: pd.Series) -> None:
    indexes, columns = load_json(METRICS_PATH)
    for key in columns.keys():
        columns[key].append(dict(new_metrics)[key])
    print(columns)
    indexes["index"].append(MODEL_PATH)
    save_json(METRICS_PATH, [indexes, columns])


def clean_metrics():
    metrics_template = [{"index": []}, DICT_TEMPLATE]
    save_json(METRICS_PATH, metrics_template)


if __name__ == "__main__":
    ethalons = load_json(ETHALONS_PATH)
    scores = count_scores(ethalons)
    # clean_metrics()
    # save_json(SCORES_PATH, scores)

    scores_series = make_scores_series(scores, DICT_TEMPLATE)
    append_metrics(scores_series)
    print(scores_series)
