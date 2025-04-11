# CLO835FinalProject

## 1. MySQL database
Test locally using docker 
```
cd db
docker build -t my_db .
docker network create mynet
docker run --name mysql --network mynet -d -e MYSQL_ROOT_PASSWORD=pw my_db
```


## 2. Flask App with external background images
Test locally using docker 
```
cd app
docker build -t my_app .
docker inspect mysql
docker run --name app --network mynet -d -e DBHOST=<mysql-ip> -p 8080:8080 my_app
```


## 3. Push docker images, `my-db` and `my-app`, into ECR repos


# Deployment

## Using kind cluster

```
kind create cluster --config kind.yaml
k create ns final
k create secret generic creds-final --from-file=.dockerconfigjson=/home/ec2-user/.docker/config.json --type=kubernetes.io/dockerconfigjson -n final
k apply -f db_deployment.yaml
k apply -f db_service.yaml
k apply -f pvc.yaml
k apply -f configmap.yaml 
k apply -f app_deployment.yaml
k apply -f app_service.yaml
```