from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ReceiversBase(BaseModel):
    document_number: Optional[str]
    name: Optional[str]
    creation_date: Optional[datetime]
    modification_date: Optional[datetime]

class ReceiversCreate(ReceiversBase):
    pass

class ReceiversUpdate(ReceiversBase):
    document_number: Optional[str]
    name: Optional[str]

class Receivers(ReceiversBase):
    id: int

    class Config:
        orm_mode = True