#!/bin/bash

set -e

if ! minikube status | grep -q "cluster: Running"; then
    echo "***** Starting minikube cluster *****";
    minikube start --memory=2048 --cpus=2;
fi

echo "***** Launching kubernetes services *****"
kubectl apply -f k8s/

echo "***** Waiting for the application to start. This may take up to ten minutes *****"
kubectl rollout status deployment/horangi-demo

kubectl exec cassandra-0 -- cqlsh -e "$(cat scripts/init.cql)"

echo "The service is available at $(minikube service horangi-demo --url)/api/users/"
