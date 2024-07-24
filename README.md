# quotes
FastAPI quote app

## local set up 
set up local pod, container and db. 
`podman pod create -p 8000:8000 -p 5432:5432 --name=quote_pod && podman pod start quote_pod`
`podman build -t quote-app -f Dockerfile --ignorefile .dockerignore`
`podman run -d --pod=quote_pod --name=postgres_db -v dbdata:/var/lib/postgresql/data  --env-file src/core/.env docker.io/postgres:latest`
`podman run -d --pod=quote_pod --name=quote-app quote-app`
    

# Podman   

Set up pod to put all related app containers together, like docker compose.  Note mapped ports are only declared at the top level , rather the pod the containers are in.

// moving this pod building to a start up script

oracle vps setup

```  
sudo firewall-cmd --permanent --zone=public --add-port=80/tcp
sudo firewall-cmd --permanent --zone=public --add-port=443/tcp
sudo firewall-cmd --runtime-to-permanent
```

### create systemd services
Using the user flag, these generated files get stored here [podman docs](https://docs.podman.io/en/latest/markdown/podman-generate-systemd.1.html)  

`podman generate systemd --files --name quote_pod`
copy files
`mv -v *.service ~/.config/systemd/user/`

enable/disable
`systemctl --user enable pod-quote_pod.service`

enable linger  
`loginctl enable-linger $USER`

and start
`systemctl --user start pod-quote_pod.service`

check running
`systemctl --user --type=service --state=running`


### Docker 
[Docker set up here](DOCKER.md)

## running jobs 

call scraper via container. Use this in the crontab job. 

`podman exec quote-app python -m scraper`

### check db in container

`psql -U $POSTGRES_USER $POSTGRES_DB`
