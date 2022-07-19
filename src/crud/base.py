from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from src.db import dynamo


CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[CreateSchemaType, UpdateSchemaType]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).
    """

    def get(self, db: dynamo, primaryKey: dict) -> Optional[dict]:
        response = db.get_item(Key={**primaryKey})
        item = response["Item"]
        return item

    def get_multi(self, db: dynamo, *, skip: int = 0, limit: int = 100) -> List[dict]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: dynamo, *, obj_in: CreateSchemaType) -> Any:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: dynamo,
        *,
        db_obj: Any,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> Any:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: dynamo, *, id: int) -> Any:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
