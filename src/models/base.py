class BaseDBModel:
    def __init__(self, attrs: dict):
        for i, j in attrs.items():
            setattr(self, i, j)

    def to_dict(self):
        return self.__dict__
