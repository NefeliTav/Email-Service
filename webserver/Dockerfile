FROM python:3.7-stretch

COPY . .

RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate
#RUN python manage.py collectstatic --no-input

#CMD python manage.py runserver 0.0.0.0:8000
CMD gunicorn project.wsgi:application --bind 0.0.0.0:8000 --timeout 0
