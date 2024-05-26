#!/bin/bash

### set up environment and load up pod containers. 
echo "Creating volument 'letsencrypt'"
podman volume create letsencrypt

echo "Create pod quote_pod"
podman pod create -p 8080:80 -p 8081:443 --name=quote_pod

echo "Starting quote pod..."
podman pod start quote_pod 

echo "Building quote app container..."
podman build -t quote-app -f Dockerfile

echo "Starting Caddy webserver container in pod"
podman run -d --pod=quote_pod \
    -v $PWD/Caddyfile:/etc/caddy/Caddyfile:z \
    -v letsencrypt:/data \
    docker.io/library/caddy:2.7.6-alpine

echo "Spinning up postgres container"
podman run -d --pod=quote_pod --name=postgres_db -v dbdata:/var/lib/postgresql/data  --env-file core/.env docker.io/postgres:latest

echo "Spin up quotes app"
podman run -d --pod=quote_pod --name=quote-app quote-app
