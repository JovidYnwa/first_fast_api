from fastapi import APIRouter
from populate import calculate_gem_price
import repos.gem_repository 
from models.gem_models import *
from db.db import session

from starlette.status import HTTP_204_NO_CONTENT
from fastapi.encoders import jsonable_encoder

gem_router = APIRouter()

@gem_router.get('/gems')
def gems():
    """hey hey"""
    gems = repos.gem_repository.select_all_gems()
    return {"gems":gems}

@gem_router.get('/gem/{id}', tags=['Gems'])
def gems(id: int):
    """hey hey"""
    gems = repos.gem_repository.select_gem(id=id)
    return {"gems":gems}


@gem_router.post('/gems', tags=['Gems'])
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


@gem_router.put('/gems/{id}', response_model=Gem, tags=['Gems'])
def update_gem(id: int, gem: Gem):
    gem_found = session.get(Gem, id)

    update_item_encoded = jsonable_encoder(gem)
    update_item_encoded.pop('id', None)
    for key, val in update_item_encoded.items():
        gem_found.__setattr__(key, val)
    session.commit()
    return gem_found


@gem_router.patch('/gems/{id}', response_model=Gem, tags=['Gems'])
def patch_gem(id: int, gem: GemPatch, ):
    gem_found = session.get(Gem, id)

    update_data = gem.dict(exclude_unset=True)
    update_data.pop('id', None)
    for key, val in update_data.items():
        gem_found.__setattr__(key, val)
    session.commit()
    return gem_found


@gem_router.delete('/gems/{id}', status_code=HTTP_204_NO_CONTENT, tags=['Gems'])
def delete_gem(id:int,):
    gem_found = session.get(Gem, id)

    session.delete(gem_found)
    session.commit()
