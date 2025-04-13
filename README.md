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
docker run --name app --network mynet -d -e DBHOST=<mysql-ip> -p 81:81 my_app
```


## 3. Push docker images, `my_db` and `my_app`, into ECR repos (manually or via GitHub Actions)


# Deployment

## In kind cluster


## In Amazon EKS

### 1. Cloud 9 Pre-requisites (only once per Cloud9 environment)

```
# Configure your permanent credentials and disable Cloud9 temporary credentials
/usr/local/bin/aws cloud9 update-environment --environment-id $C9_PID --managed-credentials-action DISABLE

# Clear current credentials file
> -vf ${HOME}/.aws/credentials

# Use credentials from AWS Academy AWS Details and copy them into ~/.aws/credentials file
vi ~/.aws/credentials 

# Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv -v /tmp/eksctl /usr/local/bin
```

### 2. Create EKS cluster

```
# Replace AWS Account ID
eksctl create cluster -f eks_config.yaml
```

- Cleanup if necessary
    ```
    eksctl delete cluster --region=us-east-1 --name=eks-cluster
    ```

### 3. Bootstrap

- Create namespace `final`, ServiceAccount `clo835`, ClusterRole and ClusterRoleBinding.
```
k apply -f bootstrap.yaml
```

### 4. Deploy application

#### Refresh `secret_ecr.yaml` for a new session

1. Generate the secret manifest by running script `get_ecr_secret.sh`

2. Create ECR secret

    ```
    k apply -f secret_ecr.yaml
    ```

#### Deploy app
```
k apply -f pvc.yaml
k apply -f db_deployment.yaml
k apply -f db_service.yaml
k apply -f configmap.yaml 
k apply -f secret_db.yaml
k apply -f secret_aws.yaml
k apply -f secret_ecr.yaml
k apply -f app_deployment.yaml
k apply -f app_service.yaml
```


> [!NOTE] 
- Modify `secret_aws.yaml` with <AWS_ACCESS_KEY_ID>, <AWS_SECRET_ACCESS_KEY> and <AWS_SESSION_TOKEN>.


- Verify background image log entries
```
k logs <pod-name> -n final
```
