#!/bin/bash
AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_PASSWORD=$(aws ecr get-login-password --region $AWS_REGION)
ECR_REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
# Generate the secret with kubectl
kubectl create secret docker-registry ecr-credentials \
  --docker-server=$ECR_REGISTRY \
  --docker-username=AWS \
  --docker-password=$ECR_PASSWORD \
  --docker-email=jguo73@myseneca.ca \
  --namespace=final \
  --dry-run=client -o yaml > secret_ecr.yaml
