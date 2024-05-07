
import pytz
from datetime import datetime
from src.adapters.orm_base import OrmBaseModel
from sqlalchemy import DDL, event, Column, Integer, String, DateTime

"""
ORM class to interact with the Receivers table in the database
"""
class Receivers(OrmBaseModel):
    __tablename__ = 'receivers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_number = Column(String(255), nullable=False, unique=True)
    name = Column(String(150), nullable=False)
    creation_date = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))
    modification_date = Column(DateTime(timezone=True), default=datetime.now(pytz.utc))

    
restart_seq = DDL("ALTER SEQUENCE %(table)s_id_seq RESTART WITH 100;")

event.listen(
    Receivers.__table__, "after_create", restart_seq.execute_if(dialect="mysql")
)    