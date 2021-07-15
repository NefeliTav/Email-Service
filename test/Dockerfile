FROM python:3
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
ADD ./ /app
WORKDIR /app

CMD ["python","-u","webserver.py"]