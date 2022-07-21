from pydantic import BaseModel


class JsonMsg(BaseModel):
    msg: str
