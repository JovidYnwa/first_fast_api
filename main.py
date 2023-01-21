from fastapi import FastAPI
import uvicorn
from db.db import engine
import repos.gem_repository 
from sqlmodel import create_engine, SQLModel
from models.gem_models import *

app = FastAPI()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.get('/gems')
def gems():
    """hey hey"""
    gems = repos.gem_repository.select_all_gems()
    return {"gems":gems}

@app.get('/gem/{id}')
def gems(id: int):
    """hey hey"""
    gems = repos.gem_repository.select_gem(id=id)
    return {"gems":gems}

if __name__ == "__main__":
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    create_db_and_tables()