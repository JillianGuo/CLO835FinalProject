# CLO835FinalProject

> [!NOTE] alias k=kubectl


## 1. Create EKS cluster if not created yet

```
eksctl create cluster -f eks_config.yaml
```

## 2. Bootstrap

- Create namespace `final`, ServiceAccount `clo835`, ClusterRole and ClusterRoleBinding.

```
k apply -f bootstrap.yaml
```

## 3. Create ConfigMap and Secrets

> [!NOTE] 
- Modify `secret_aws.yaml` with <AWS_ACCESS_KEY_ID>, <AWS_SECRET_ACCESS_KEY> and <AWS_SESSION_TOKEN>.

```
k apply -f configmap.yaml
k apply -f secret_db.yaml
k apply -f secret_aws.yaml
```

## 4. Create the ECR imagePullSecret (for a new session)

Step 1. Generate the secret manifest by running script `get_ecr_secret.sh`

```
chmod +x get_ecr_secret.sh  # if not executive
./get_ecr_secret.sh
```

Step 2. Create ECR secret

```
k apply -f secret_ecr.yaml
```

## 5. Create the PersistentVolumeClaim

```
k apply -f pvc.yaml
```

- Install the AWS EBS CSI Driver if not installed for the cluster

```
eksctl create addon \
  --name aws-ebs-csi-driver \
  --cluster eks-cluster \
  --region us-east-1 \
  --force
```


## 6. Deploy the MySQL database
```
k apply -f db_deployment.yaml
k apply -f db_service.yaml
```

- Verification
```
k get pods -n final
k get svc -n final
```

## 7. Deploy the application
```
k apply -f app_deployment.yaml
k apply -f app_service.yaml
```

- Verification
```
k get pods -n final
k get svc -n final
```

## 8. Get public endpoint and verify it in a browser
```
k get svc app-svc -n final
```

## 9. Verify background image log entries
```
k logs <pod-name> -n final
```

## 10. Rollout for another background image

- Modify `configmap.yaml` and apply it
```
k apply -f configmap.yaml
```

- Rollout
```
k rollout restart deployment clo835-final-app -n final
```

- Verify logs
```
k logs <pod-name> -n final
```

## 11. Cleanup if necessary
```
eksctl delete cluster --region=us-east-1 --name=eks-cluster
```

For testing