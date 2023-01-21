from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum, IntEnum


class GemTypes(str, Enum):
    DIAMOND = 'DIAMON'
    RUBY = 'RUBY'
    EMERALD = 'EMERALD'


class GemClarity(IntEnum):
    SI = 1
    VS = 2
    VVS = 3
    FL = 4


class GemColor(str, Enum):
    D = 'D'
    E = 'E'
    G = 'G'
    F = 'F'
    H = 'H'
    I = 'I'


class GemProperties(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    size: float = 1
    clarity: Optional[GemClarity] = None
    color: Optional[GemColor] = None


class Gem(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    price: float
    available: bool = True
    gem_type: GemTypes = GemTypes.DIAMOND #default val

    #creating foregin keys
    gem_properties_id: Optional[int] = Field(default=None, foreign_key='gemproperties.id')

