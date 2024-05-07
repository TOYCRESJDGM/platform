import pytz
from datetime import datetime
from sqlalchemy.orm import relationship
from src.adapters.orm_base import OrmBaseModel
from sqlalchemy import DDL, event, Column, Integer, String, Date, ForeignKey, DateTime

"""
ORM class to interact with the invoice table in the database
"""
class Invoice(OrmBaseModel):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number_invoice = Column(String(255), nullable=False)
    date_issued = Column(Date, nullable=False)
    pdf_url = Column(String(255))
    emitter_id = Column(Integer, ForeignKey('emitters.id'))
    receiver_id = Column(Integer, ForeignKey('receivers.id'))
    series = Column(String(10))
    folio = Column(Integer)
    tax = Column(Integer)
    total = Column(Integer)
    creation_date = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))
    modification_date = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))

    # Define las relaciones con los emisores y receptores
    emitter = relationship("Emitters")
    receiver = relationship("Receivers")


restart_seq = DDL("ALTER SEQUENCE %(table)s_id_seq RESTART WITH 100;")

event.listen(
    Invoice.__table__, "after_create", restart_seq.execute_if(dialect="mysql")
)