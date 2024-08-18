import json
import warnings

import spacy
from spacy.tokens import DocBin

ROW_DATA_PATH = "data/train.json"
BINARY_DATA_PATH = "./binary/train.spacy"


def spacy_data_from_ls(ls_data: list) -> list:
    train_data = []
    for sample in ls_data:
        text = sample["data"]["text"]
        entities = []
        for ent in sample["annotations"][0]["result"]:
            new = (ent["value"]["start"], ent["value"]["end"], ent["value"]["labels"][0])
            entities.append(new)
        train_data.append([text, {"entities": entities}])
    return train_data


def convert(lang: str, TRAIN_DATA, output_path: str):
    nlp = spacy.blank(lang)
    db = DocBin()
    for text, annot in TRAIN_DATA:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                warnings.warn(msg)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)


def make_binary_from_ls():
    with open(ROW_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    train_data = spacy_data_from_ls(data)
    convert("ru", train_data, BINARY_DATA_PATH)


if __name__ == "__main__":
    make_binary_from_ls()
