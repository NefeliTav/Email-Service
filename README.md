# Email-Service

## Setup

```
pip install -r requirements.txt
```

## Run

Webserver, antispam, emaildb, userdb

```
docker-compose up
```

## Stress-test

Run
```
locust -f webserver/locust_test.py
```
and then open [web-interface](http://127.0.0.1:8089/). Default port is 8001.
