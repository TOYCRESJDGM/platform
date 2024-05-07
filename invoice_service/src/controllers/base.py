from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.adapters.orm_base import OrmBaseModel

ModelType = TypeVar("ModelType", bound=OrmBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

"""
Base CRUD Model for SQLAlchemy ORM
"""

class BaseController(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model_cls: Type[ModelType]):  # 2
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model_cls = model_cls

    def get(self, db: Session, model_id: Any) -> Optional[ModelType]:
        """
        Get a record by its id.
        :param db:
        :param model_id:
        :return:
        """
        return db.query(self.model_cls).filter_by(id=model_id, deleted=False).first()

    def fetch_all(self, db: Session) -> list[tuple[Any]]:
        """
        Read all records.
        :param db:
        :return:
        """
        return db.query(self.model_cls).filter(self.model_cls.deleted == False).all()

    def create(self, db: Session, *, entity: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        :param db:
        :param entity:
        :return:
        """
        obj_in_data = jsonable_encoder(entity)
        db_obj = self.model_cls(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_batch(self, db: Session, entities: List[CreateSchemaType]):
        """
        Create a list of records.
        :param db:
        :param entities:
        :return:
        """
        objects_to_insert = []
        for entity in entities:
            existing_data = db.query(self.model_cls).filter_by(name=entity.name, region=entity.region).first()
            if not existing_data:
                objects_to_insert.append(entity)

        db_objs = list(
            map(lambda entity_insert: self.model_cls(**jsonable_encoder(entity_insert)), objects_to_insert)
        )
        db.bulk_save_objects(db_objs)
        db.commit()

    def update(
        self, db: Session, *, model_id: Any, entity: UpdateSchemaType
    ) -> ModelType:
        """
        Update a record.
        :param db:
        :param model_id:
        :param entity:
        :return:
        """
        db_obj = self.get(db, model_id)
        if db_obj is None:
            raise Exception("Object not found")
        obj_in_data = jsonable_encoder(entity)
        for key, value in obj_in_data.items():
            setattr(db_obj, key, value if value is not None else getattr(db_obj, key))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def soft_delete(self, db: Session, *, model_id: Any, entity: UpdateSchemaType) -> ModelType:
        """
        Soft delete a record.
        """
        db_obj = self.get(db, model_id)
        if db_obj is None:
            raise Exception("Object not found")

        setattr(db_obj, "deleted", True)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
    
    def delete(self, db: Session, model_id: Any) -> Optional[ModelType]:
        """
        delete a record.
        :param db:
        :param model_id:
        :return:
        """
        db_obj = self.get(db, model_id)
        if db_obj is None:
            raise Exception("Object not found")
        db.delete(db_obj)
        db.commit()
        return