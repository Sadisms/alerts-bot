import peewee


conn = peewee.SqliteDatabase(
    database='._.db'
)


class BaseModel(peewee.Model):
    """ Базовая модель """

    class Meta:
        database = conn
