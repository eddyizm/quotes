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

## Docker build and run
`docker build -t quote_api .`  

`docker run -d -p 5432:8000 quote_api`  
*using this port on my local dev machine to validate*  

## Docker Compose  
`docker compose up --build -d`

## running jobs 

call scraper via docker. Use this in the crontab job. 

`docker exec -it <CONTAINER ID> python -m scraper`
