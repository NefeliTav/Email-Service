FROM python:3
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
ADD ./ /app
WORKDIR /app
RUN pip install -r requirements.txt

RUN python src/manage.py makemigrations
RUN python src/manage.py migrate
CMD ["python","-u","src/manage.py", "runserver", "0.0.0.0:80"]



#docker build -f Dockerfile -t emailservice:latest .
#docker run -p 8000:8000 emailservice:latest