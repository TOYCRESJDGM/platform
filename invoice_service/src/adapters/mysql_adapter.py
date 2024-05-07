from sqlalchemy import create_engine, event
from sqlalchemy.orm import (
    sessionmaker,
)  # create a session factory to connect to the database
from src.utils.settings import ( 
    DB_NAME,
    DB_HOST,
    DB_USER,
    DB_PASSWORD
)
from src.utils.logger import logger
from sqlalchemy.exc import OperationalError
from functools import wraps
from .orm_base import OrmBaseModel

SQLALCHEMY_DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
logger.debug(f"SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")

try:
    engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Realizar ping al servidor para comprobar la conexión antes de la ejecución de la consulta
    pool_size=5,  # Tamaño del conjunto de conexiones
    max_overflow=10,  # Número máximo de conexiones que pueden estar ocupadas al mismo tiempo
    pool_timeout=30  # Número máximo de segundos para esperar la adquisición de una nueva conexión de la piscina
)
except OperationalError as e:
    logger.error(f"Error connecting to the database: {e}")

def on_connect(dbapi_con, con_record):
    logger.debug(f"connection established to database {dbapi_con}")

event.listen(engine, "connect", on_connect)

# connect factory to the database
SessionMaker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)

def create_session(func):
    """
    Create a database session
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        session = SessionMaker()
        try:
            result = func(*args, session=session, **kwargs)
            session.commit()
            return result
        except:
            session.rollback()
            raise
        finally:
            session.close()

    return wrapper


def create_db():
    """
    Create all tables in the database
    :return:
    """
    OrmBaseModel.metadata.create_all(bind=engine)

class DBConnection:
    def __init__(self):
        self.db = SessionMaker()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    with DBConnection() as db:
        yield db


def get_db_session():
    """
    Get the database session.
    :return:
    """
    try:
        db = SessionMaker()
        yield db
    finally:
        db.close()