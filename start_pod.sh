#!/bin/bash

### set up environment and load up pod containers. 

echo "Create pod quote_pod"
podman pod create -p 8000:8000 --name=quote_pod \
&& \
podman pod start quote_pod 

echo "Building quote app container..."
podman build -t quote-app -f Dockerfile

echo "Spinning up postgres container"
podman run -d --pod=quote_pod --name=postgres_db -v dbdata:/var/lib/postgresql/data  --env-file src/core/.env docker.io/postgres:latest

echo "Spin up quotes app"
podman run -d --pod=quote_pod --name=quote-app quote-app

echo "generating quote_pod systemd files"

podman generate systemd --new --files --name quote_pod

echo "copy generated new service files"

mv -v *.service ~/.config/systemd/user/

echo "stop running pods"

podman stop quote-app
podman stop postgres_db

echo "enable pod/container services"

systemctl --user enable pod-quote_pod.service

echo "enable linger for user"

loginctl enable-linger $USER

echo "starting pod service"

systemctl --user start pod-quote_pod.service
