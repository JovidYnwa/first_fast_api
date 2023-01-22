from db.db import engine
 
from models.gem_models import Gem, GemProperties
from sqlmodel import Session, select

'''Examples of queries        
Conditions  SqlAchemy                                         RawSql
(where)     select(Gem).where(Gem.id == 1)                   => select * from gem g where g.id =1;
(where and) select(Gem).where(Gem.id == 1).wehre(Gem.id < 10)=> select * from gem g where g.id =1 and g.id <10;
(joins)     select(Gem, GemProperties)                       => select * from gem g join gemproperties gp
            .where(Gem.id == GemProperties.id)                               on g.gem_properties.id = gp.id;

'''

def select_all_gems():
    with Session(engine) as session:
        statement = select(Gem, GemProperties).where(Gem.gem_properties_id==GemProperties.id)
        result = session.exec(statement)
        return result.all()

def select_gem(id: int):
    with Session(engine) as session:
        statement = select(Gem).where(Gem.id == id)
        result = session.exec(statement)
        return result.all()


#select_all_gems()

