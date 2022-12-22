#!/bin/sh

# gcloud container clusters create mykube --preemptible --num-nodes=1 --machine-type=e2-standard-16 --release-channel None --zone us-central1-b
# gcloud container clusters update mykube --update-addons=HttpLoadBalancing=ENABLED
# gcloud container clusters get-credentials mykube --zone us-central1-b
# helm repo add bitnami https://charts.bitnami.com/bitnami
# helm install -f minio/minio-config.yaml -n minio-ns --create-namespace minio-proj bitnami/minio

kubectl apply -f redis/redis-deployment.yaml
kubectl apply -f redis/redis-service.yaml

kubectl apply -f rest/rest-deployment.yaml
kubectl apply -f rest/rest-service.yaml
kubectl apply -f rest/rest-ingress.yaml

kubectl apply -f logs/logs-deployment.yaml

kubectl apply -f worker/worker-deployment.yaml

kubectl apply -f minio/minio-external-service.yaml

# kubectl port-forward -n minio-ns --address 0.0.0.0 service/minio-proj 9000:9000 &
# kubectl port-forward -n minio-ns --address 0.0.0.0 service/minio-proj 9001:9001 &