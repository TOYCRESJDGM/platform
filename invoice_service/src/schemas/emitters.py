from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class EmitterBase(BaseModel):
    document_number: Optional[str]
    name: Optional[str]
    creation_date: Optional[datetime]
    modification_date: Optional[datetime]

class EmitterCreate(EmitterBase):
    pass

class EmitterUpdate(EmitterBase):
    document_number: Optional[str]
    name: Optional[str]

class Emitter(EmitterBase):
    id: int

    class Config:
        orm_mode = True