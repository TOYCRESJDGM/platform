
import pytz
from datetime import datetime
from sqlalchemy.orm import relationship
from src.adapters.orm_base import OrmBaseModel
from sqlalchemy import DDL, event, Column, Integer, String, ForeignKey, DateTime

"""
ORM class to interact with the events table in the database
"""
class Event(OrmBaseModel):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    code = Column(String(255), nullable=False)
    description = Column(String(255))
    date_event = Column(DateTime, nullable=False)
    creation_date = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))
    modification_date = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))

    # Define la relación con la tabla de factura
    invoice = relationship("Invoice")


restart_seq = DDL("ALTER SEQUENCE %(table)s_id_seq RESTART WITH 100;")

event.listen(
    Event.__table__, "after_create", restart_seq.execute_if(dialect="mysql")
)