import json

import pandas as pd
import spacy

EXCEL_PATH = "test_dataset/eval_data.xlsx"
MODEL_PATH = "models/model-best"
MODEL_ANNOTATED_PATH = "test_dataset/model_annotated.json"


def save_json(path: str, object_name) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(object_name, file, ensure_ascii=False)


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as file:
        obj = json.load(file)
    return obj


def exel2json(excel_path: str) -> list:
    """Формируем json, представляющий собой
    список текстов
    """
    df = pd.read_excel(excel_path)
    texts_list = [col["full_text"] for _, col in df.iterrows()]
    return texts_list


def model_annotation(model_path, texts_list):
    """Размечает тексты моделью
    Требует ручной проверки после разметки
    Формат выдачи
    [
        [
            'text',               - Чистый текст
            {
                "entities": [     - Размеченные моделью сущности
                    [
                        1,
                        2,
                        "ORG",
                        "Русал"
                    ]
                ]
            },
            [
                (1,"Русал"),      - Нумерация токенов для ручного исправления
                (2, "растет")
            ]
        ]
    ]"""
    model_annotated_texts = []
    nlp = spacy.load(model_path)
    for text in texts_list:
        pred_doc = nlp(text)
        words = [(v, x.text) for v, x in enumerate(pred_doc)]
        response = [[entity.start, entity.end, entity.label_, entity.text] for entity in pred_doc.ents]
        model_annotated_texts.append([text, {"entities": response}, words])
    return model_annotated_texts


if __name__ == "__main__":
    # Выполнить ДО ручной проверки
    texts_list = exel2json(EXCEL_PATH)
    model_annotated_texts = model_annotation(MODEL_PATH, texts_list)
    save_json(MODEL_ANNOTATED_PATH, model_annotated_texts)
    print("model_annotated_texts are saved")
