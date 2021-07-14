FROM python:3.7-stretch

WORKDIR /home/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

CMD python app.py
