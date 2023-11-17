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
## db migrations with Alembic  
Set this up after starting project. After installing, set up locally  

`alembic init alembic`  

Show current

`alembic current`  
and then history  
`alembeic hsitory`  
Now upgrade to the latest, similar to a `git pull`  
`alembic upgrade head`   
*This command is setup to run in the docker container for any migrations made outside.*

Downgrade to a previous version  
`alembic downgrade -1`

Create new migration  
`alembic revision -m "<YOUR MESSAGE>"`  

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
`sudo podman build -t quote_app -f Dockerfile`

`podman pod create -p 8080:80 -p 8081:443 --name=quote_pod`  

and nginx container in pod
`podman run -d --pod=quote_pod --restart=unless-stopped --name=reverse-proxy docker.io/library/nginx:1.25.3-alpine-slim`

`podman run -d --pod=quote_pod --name=postgres_db --restart=unless-stopped -v dbdata:/var/lib/postgresql/data  --env-file core/.env docker.io/postgres:latest`

`podman run -d --pod=quote_pod --name=quote-app --restart=unless-stopped quote-app`

oracle vps setup

```  
sudo firewall-cmd --add-masquerade
sudo firewall-cmd --permanent --zone=public --add-port=80/tcp
sudo firewall-cmd --list-forward-ports
```
