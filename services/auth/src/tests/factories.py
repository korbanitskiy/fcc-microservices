import asyncio
import inspect

from factory import Sequence
from factory.base import Factory

from auth.models import User
from auth.services import get_password_hash


class OrmarFactory(Factory):
    class Meta:
        abstract = True

    @classmethod
    async def _save_obj(cls, model, *args, **kwargs):
        for key, value in kwargs.items():
            if inspect.isawaitable(value):
                kwargs[key] = await value

        return await model.objects.create(*args, **kwargs)

    @classmethod
    def _create(cls, model_class, *args, **kwargs) -> asyncio.Task:
        # A Task can be awaited multiple times, unlike a coroutine.
        # useful when a factory and a subfactory must share a same object
        return asyncio.create_task(cls._save_obj(model_class, *args, **kwargs))

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]


class UserFactory(OrmarFactory):
    class Meta:
        model = User

    name = Sequence(lambda n: f"user_name-{n}")
    password = get_password_hash("password")
    disabled = False
