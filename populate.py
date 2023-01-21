import random
import string
from sqlmodel import Session

from main import engine
from models.gem_models import Gem, GemProperties

color_grades = string.ascii_uppercase[3:9]


def create_gem_props():
    size = random.randint(3, 70)/10
    color = color_grades[random.randint(0,5)]
    clarity = random.randint(1,4)
    gemp_p = GemProperties(size=size, clarity=clarity,
     color=color)
    return gemp_p


def create_gem(gem_p):
    gem = Gem(price=1000, gem_properties_id=gem_p)    
    return gem


def create_gems_db():
    gem_p = create_gem_props()
    print(gem_p)
    with Session(engine) as session:
        session.add(gem_p)
        session.commit

        g = create_gem(gem_p.id)
        session.add(g)
        session.commit()

create_gems_db()

