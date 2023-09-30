import ormar
from auth.app import database, metadata


class OrmarMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(OrmarMeta):
        tablename = "user"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=128, unique=True, min_length=6)
    password: str = ormar.String()
    disabled: bool = ormar.Boolean()
