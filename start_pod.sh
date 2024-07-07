#!/bin/bash

### set up environment and load up pod containers. 

echo "Create pod quote_pod"
podman pod create -p 8000:8000 --name=quote_pod

echo "Starting quote pod..."
podman pod start quote_pod 

echo "Building quote app container..."
podman build -t quote-app -f Dockerfile

echo "Spinning up postgres container"
podman run -d --pod=quote_pod --name=postgres_db -v dbdata:/var/lib/postgresql/data  --env-file src/core/.env docker.io/postgres:latest

echo "Spin up quotes app"
podman run -d --pod=quote_pod --name=quote-app quote-app
