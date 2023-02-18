from fastapi import FastAPI

from schema import users

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}