FROM python:3.9

WORKDIR /usr/src

COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app ./app
COPY ./data ./data
COPY ./sql_base ./sql_base

RUN cp -f sql_base/base.py /usr/local/lib/python3.9/site-packages/sqlalchemy/dialects/postgresql

WORKDIR /usr/src/app

EXPOSE 5000

CMD ["python3", "parser_server_app.py"]
