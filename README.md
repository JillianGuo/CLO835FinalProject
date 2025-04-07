# CLO835FinalProject

## 1. MySQL database

## 2. Flask App with external background images

# Deployment

## Using kind cluster

```
kind create cluster --config kind.yaml
k create ns test
k create secret generic creds-final --from-file=.dockerconfigjson=/home/ec2-user/.docker/config.json --type=kubernetes.io/dockerconfigjson -n test
k apply -f db_deployment.yaml
k apply -f db_service.yaml
k apply -f app_deployment.yaml
k apply -f app_service.yaml
```