FROM python:3.9

COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY ./server-app ./server-app
COPY ./train ./train
COPY ./models ./models

WORKDIR /usr/src/server-app

EXPOSE 5000

CMD ["python3", "spacy_server.py"]
