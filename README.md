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


# Podman   

Set up pod to put all related app containers together, like docker compose.  Note mapped ports are only declared at the top level , rather the pod the containers are in.

// moving this pod building to a start up script

oracle vps setup

```  
sudo firewall-cmd --permanent --zone=public --add-port=80/tcp
sudo firewall-cmd --permanent --zone=public --add-port=443/tcp
sudo firewall-cmd --add-forward-port=port=80:proto=tcp:toport=8080
sudo firewall-cmd --add-forward-port=port=443:proto=tcp:toport=8081
sudo firewall-cmd --add-masquerade
sudo firewall-cmd --list-forward-ports
sudo firewall-cmd --runtime-to-permanent
```

### create systemd services
Using the user flag, these generated files get stored here [podman docs](https://docs.podman.io/en/latest/markdown/podman-generate-systemd.1.html)  
`.config/systemd/user`

check running
`systemctl --user --type=service --state=running`

enable/disable
`systemctl --user enable container-quote-app.service`


### Docker 
[Docker set up here](DOCKER.md)

## running jobs 

call scraper via container. Use this in the crontab job. 

`podman exec quote-app python -m scraper`
