# Pipeline обучения модели NER из SPACY
Обучение состоит из нескольких шагов:  
1. Разметка в Label Studio
2. Трансформация разметки в формат [[text, {"entities": [[start_pos, end_pos, label]]}]]
3. Трансформация в бинарную разметку
4. Обучение модели
5. Вызов модели

## Трансформации разметки
`python make_binary_data.py`

В результате работы скрипта появится файл `./binary/train.spacy` 

## Перед обучением
Зайти на сайт разработчиков, установить параметры, скачать basic_config  
https://spacy.io/usage/training  

Создать config 
`python -m spacy init fill-config base_config.cfg config.cfg`

## Запуск обучения
`python3 -m spacy train config.cfg --output ./models --paths.train ./binary/train.spacy`

## Вызов модели
```
import spacy
nlp = spacy.load("models/model-best")
doc = nlp("Идея от брокера Распадская рост на 18: срок 4 месяца #DFRT")
for entity in doc.ents:
    print(entity.text, entity.label_)
```
## Запуск в докере
Сбор контейнера  
`docker build -t spacy-app:v1 -f Dockerfile .`  
Запуск в интерактивном режиме  
`docker run --rm -it --name spacy-app -v "$PWD":/app -p 8568:5000 spacy-app:v1 bash`  
Запуск в демоне  
`docker run -d --name spacy-app -v "$PWD":/app -p 8568:5000 spacy-app:v1`  

## Описание файлов
```
|-binary
....|- train.spacy                            - бинарные данные для обучения (полные)
|- data
....|- 1_row_data_for_ls.json                 - для загрузки в label studio (образец)
....|- 2_ls_annotated_data.json               - размеченные в label studio (образец)
....|- 3_spacy_annotated_train_data.json      - разметка для spacy которая может быть перобразована в бинарную (образец)
|- models
....|- model-best                             - используемая модель
....|- model-last                             - создается при обучении
|- base_config.cfg                            - файл загружаемый от разработчиков
|- config.cfg                                 - файл формируется на основе basic_config
|- client.py                                  - образец обращения к сервису
|- Dockerfile
|- make_binary_data.py                        - создание бинарной даты из разметки в label studio
|- README.md
|- requirements.txt
|- spacy_server.py                            - запуск серверной части
```
