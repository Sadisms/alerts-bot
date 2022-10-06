from datetime import datetime

import peewee

from .base import BaseModel


class Users(BaseModel):
    id = peewee.PrimaryKeyField()
    user_id = peewee.IntegerField()
    file = peewee.TextField(null=True)
    date_join = peewee.DateTimeField(default=datetime.now)
    repeat = peewee.BooleanField(default=True)


class Settings(BaseModel):
    id = peewee.PrimaryKeyField()
    type = peewee.CharField()
    name = peewee.CharField()
    view_name = peewee.CharField()
    value = peewee.TextField()
