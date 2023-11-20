# quotes
FastAPI quote app

## local set up without docker

create virtual env
```  
python -m venv env
``` 
activate virtual env (linux)

```  
source env/bin/activate
``` 
activate virtual env (windows)
```
source env/Scripts/activate
```
install requirements
```
pip install -r requirements.txt
```
Launch server  
```  
uvicorn main:app --reload  
```  
---
## Docker build and run
`docker build -t quote_api .`  

`docker run -d -p 5432:8000 quote_api`  
*using this port on my local dev machine to validate*  

## Docker Compose  
`docker compose up --build -d`

## running jobs 

call scraper via docker. Use this in the crontab job. 

`docker exec -it <CONTAINER ID> python -m scraper`

export db 
`docker cp <container-id>:/usr/src/app/core/schema/quotes_app.sqlite3 ./quotes_app.sqlite3_$(date +"%m-%d-%Y")`

## setup ssl certbot
run script in root this may be retired in the podman setup

# Podman   

Set up pod to put all related app containers together, like docker compose.  Note mapped ports are only declared at the top level , rather the pod the containers are in.

Build quote app image first
`podman build -t quote-app -f Dockerfile`

`podman pod create -p 8080:80 -p 8081:443 --name=quote_pod`  

and nginx container in pod
`podman run -d --pod=quote_pod -v --name=reverse-proxy docker.io/library/nginx:1.25.3-alpine-slim`

podman run -d --pod=quote_pod --name=reverse-proxy docker.io/library/nginx:1.25.3-alpine-slim

`podman run -d --pod=quote_pod --name=postgres_db -v dbdata:/var/lib/postgresql/data  --env-file core/.env docker.io/postgres:latest`

`podman run -d --pod=quote_pod --name=quote-app quote-app`

oracle vps setup

```  
sudo firewall-cmd --add-masquerade
sudo firewall-cmd --permanent --zone=public --add-port=80/tcp
sudo firewall-cmd --list-forward-ports
```

### SSL
created volume to store certificates
`podman volume create letsencrypt`
build image
`podman build -t reverse-proxy -f nginx-dockerfile`
then run it
`podman run -d --pod=quote_pod -v $(pwd)/letsencrypt:/etc/letsencrypt --name=reverse-proxy  reverse-proxy`