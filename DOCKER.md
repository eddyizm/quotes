# Docker setup

This is currently out of date since I switched over to podman

TODO - Update docs to get back up and running on a docker system

## Docker build and run
`docker build -t quote_api .`  

`docker run -d -p 5432:8000 quote_api`  
*using this port on my local dev machine to validate*  

## Docker Compose  
`docker compose up --build -d`