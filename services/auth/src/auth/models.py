import ormar
import databases
import ormar
import sqlalchemy
import os

from auth.settings import get_app_settings

settings = get_app_settings()
metadata = sqlalchemy.MetaData()
database = databases.Database(settings.db.uri)


class OrmarMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(OrmarMeta):
        tablename = "user"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=128, unique=True, min_length=6)
    password: str = ormar.String(max_length=255)
    disabled: bool = ormar.Boolean()


# Model should be cachable for DebugToolbar tracking
if os.getenv("DEBUG"):
    ormar.Model.__hash__ = lambda self: id(self)
