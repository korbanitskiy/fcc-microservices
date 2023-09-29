import ormar
from auth.app import database, metadata


class OrmarMeta(ormar.ModelMeta):
    metadata = metadata
    database = database
