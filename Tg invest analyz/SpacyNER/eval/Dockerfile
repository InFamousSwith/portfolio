FROM spacy-app:v3

COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /usr/src

COPY . .

EXPOSE 5000

CMD ["python3", "eval_model.py"]
