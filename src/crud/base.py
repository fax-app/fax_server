from typing import Any, Dict, Generic, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[CreateSchemaType, UpdateSchemaType]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).
    """

    def get(self, db: Any, primary_key: dict) -> Optional[dict]:
        response = db.get_item(Key={**primary_key})
        item = response["Item"]
        return item

    # def get_multi(self, db: Any, *, skip: int = 0, limit: int = 100) -> List[dict]:
    #     return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Any, *, obj_in: CreateSchemaType) -> Any:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Any,
        *,
        db_obj: Any,
        obj_in: UpdateSchemaType | Dict[str, Any],
    ) -> Any:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        primary_key = db_obj.primary_key()
        update_expression = "SET"
        update_expressions = []
        expression_attribute_values = {}
        count = 1
        for field in obj_data:
            if field in update_data:
                update_expressions.append(f" {field} = :val{count}")
                expression_attribute_values[f":val{count}"] = update_data[field]
                count += 1
        update_expression += ",".join(update_expressions)

        db.update_item(
            Key=primary_key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )
        return self.get(db, primary_key)

    def remove(self, db: Any, primary_key: dict) -> Any:
        db.delete_item(Key=primary_key)
        return primary_key
