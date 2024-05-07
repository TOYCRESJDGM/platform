from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class EventInvoiceBase(BaseModel):
    invoice_id: int
    code: str
    description: Optional[str]
    date_event: datetime
    creation_date: Optional[datetime]
    modification_date: Optional[datetime]

class EventInvoiceCreate(EventInvoiceBase):
    pass

class EventInvoiceUpdate(EventInvoiceBase):
    invoice_id: Optional[int]
    code: Optional[str]
    description: Optional[str]
    date_event: Optional[datetime]

class EventInvoice(EventInvoiceBase):
    id: int

    class Config:
        orm_mode = True