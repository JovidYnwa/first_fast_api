from fastapi import FastAPI
import uvicorn
from db.db import engine
from populate import calculate_gem_price
import repos.gem_repository 
from sqlmodel import create_engine, SQLModel
from models.gem_models import *
from sqlmodel import Session

from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from fastapi.encoders import jsonable_encoder

app = FastAPI()
session = Session(bind=engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.get('/gems')
def gems():
    """hey hey"""
    gems = repos.gem_repository.select_all_gems()
    return {"gems":gems}

@app.get('/gem/{id}', tags=['Gems'])
def gems(id: int):
    """hey hey"""
    gems = repos.gem_repository.select_gem(id=id)
    return {"gems":gems}


@app.post('/gems', tags=['Gems'])
def create_gem(gem_pr: GemProperties, gem: Gem):
    """Creates gem"""


    gem_properties = GemProperties(size=gem_pr.size, clarity=gem_pr.clarity,
                                   color=gem_pr.color)
    session.add(gem_properties)
    session.commit()
    gem_ = Gem(price=gem.price, available=gem.available, gem_properties=gem_properties,
               gem_properties_id=gem_properties.id,)
    price = calculate_gem_price(gem, gem_pr)
    gem_.price = price
    session.add(gem_)
    session.commit()
    return gem


@app.put('/gems/{id}', response_model=Gem, tags=['Gems'])
def update_gem(id: int, gem: Gem):
    gem_found = session.get(Gem, id)

    update_item_encoded = jsonable_encoder(gem)
    update_item_encoded.pop('id', None)
    for key, val in update_item_encoded.items():
        gem_found.__setattr__(key, val)
    session.commit()
    return gem_found


@app.patch('/gems/{id}', response_model=Gem, tags=['Gems'])
def patch_gem(id: int, gem: GemPatch, ):
    gem_found = session.get(Gem, id)

    update_data = gem.dict(exclude_unset=True)
    update_data.pop('id', None)
    for key, val in update_data.items():
        gem_found.__setattr__(key, val)
    session.commit()
    return gem_found


@app.delete('/gems/{id}', status_code=HTTP_204_NO_CONTENT, tags=['Gems'])
def delete_gem(id:int,):
    gem_found = session.get(Gem, id)

    session.delete(gem_found)
    session.commit()


if __name__ == "__main__":
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    create_db_and_tables()