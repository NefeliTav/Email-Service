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

 - [minikube](https://minikube.sigs.k8s.io/docs/start/)
 - [kubectl](https://kubernetes.io/docs/tasks/tools/)

### Run

```
minikube start --extra-config=controller-manager.horizontal-pod-autoscaler-upscale-delay=1m --extra-config=controller-manager.horizontal-pod-autoscaler-downscale-delay=1m --extra-config=controller-manager.horizontal-pod-autoscaler-sync-period=10s --extra-config=controller-manager.horizontal-pod-autoscaler-downscale-stabilization=1m
minikube addons enable metrics-server
kubectl apply -f kubernetes
minikube service webserver --url 
```
If everything done correctly last command will return local IP with accessible application.

### Generating load
```
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://webserver; done"
```
