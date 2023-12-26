#!/bin/bash

### set up environment and load up pod containers. 
echo "Creating volument 'letsencrypt'"
podman volume create letsencrypt

echo "Create pod quote_pod"
podman pod create -p 8080:80 -p 8081:443 --name=quote_pod

echo "Create nginx container in pod"
podman run -d --pod=quote_pod -v letsencrypt:/etc/letsencrypt --name=reverse-proxy  reverse-proxy

echo "Spinning up postgres container"
podman run -d --pod=quote_pod --name=postgres_db -v dbdata:/var/lib/postgresql/data  --env-file core/.env docker.io/postgres:latest

echo "Spin up quotes app"
podman run -d --pod=quote_pod --name=quote-app quote-app

