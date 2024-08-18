FROM python:3.9

COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /usr/src

EXPOSE 5000

CMD ["streamlit", "run", "ui.py"]
