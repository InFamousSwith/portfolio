FROM python:3.9

WORKDIR /usr/src

COPY requirements.txt ./requirements.txt
RUN git config --global http.sslVerify false
RUN pip3 install --no-cache-dir -r requirements.txt
RUN git config --global http.sslVerify true
RUN pip install --no-cache-dir gunicorn

COPY ./app ./app
COPY ./sql_base ./sql_base

RUN cp -f sql_base/base.py /usr/local/lib/python3.9/site-packages/sqlalchemy/dialects/postgresql

WORKDIR /usr/src/app

EXPOSE 5000

CMD ["python3", "server_app.py"]
