FROM python:3.7-stretch

WORKDIR /home/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY wsgi.py .

CMD python app.py
CMD gunicorn --bind 0.0.0.0:5000 wsgi:app
