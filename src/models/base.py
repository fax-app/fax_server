class BaseDBModel:
    PK: str
    SK: str

    def __init__(self, attrs: dict):
        for i, j in attrs.items():
            setattr(self, i, j)

    def to_dict(self):
        return self.__dict__

    def primary_key(self):
        return {"PK": self.PK, "SK": self.SK}
