from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class InvoiceBase(BaseModel):
    number_invoice: str
    date_issued: datetime
    pdf_url: Optional[str]
    emitter_id: Optional[int]
    receiver_id: Optional[int]
    series: Optional[str]
    folio: Optional[int]
    tax: Optional[int]
    total: Optional[int]
    creation_date: Optional[datetime]
    modification_date: Optional[datetime]

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(InvoiceBase):
    number_invoice: Optional[str]
    date_issued: Optional[datetime]
    pdf_url: Optional[str]
    emitter_id: Optional[int]
    receiver_id: Optional[int]
    series: Optional[str]
    folio: Optional[int]
    tax: Optional[int]
    total: Optional[int]

class InvoiceRequest(BaseModel):
    cufes: List[str]

class ProcessInvoiceRequest(BaseModel):
    cufe: str

class Invoice(InvoiceBase):
    id: int

    class Config:
        orm_mode = True