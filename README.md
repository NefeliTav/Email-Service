# Email-Service

## Docker Compose
### Setup

```
pip install -r requirements.txt
```

### Run

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

## Kubernetes

### Prerequisites

 - [kind](https://kind.sigs.k8s.io/docs/user/quick-start/)
 - [kubectl](https://kubernetes.io/docs/tasks/tools/)

### Run

```
kind create cluster
kubectl apply -f kubernetes
kubectl port-forward service/webserver 8000:80 
```
If everything done correctly on [http://localhost:8000](http://localhost:8000) will be application accessible.
