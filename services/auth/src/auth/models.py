import ormar
from auth.app import metadata, database


class OrmarMeta(ormar.ModelMeta):
    metadata = metadata
    database = database