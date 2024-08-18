FROM python:3.9

WORKDIR /usr/src

COPY requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app ./app

WORKDIR /usr/src/app

EXPOSE 5000

CMD ["python3", "moex_server_app.py"]
