import json

from .models.base import conn
from .models.greeting_models import Users, Settings


@conn.atomic()
async def init_tables():
    conn.create_tables([Users])


@conn.atomic()
async def _get_user(user_id: int) -> Users:
    return Users.get_or_create(user_id=user_id)[0]


@conn.atomic()
async def add_user(
        user_id: int,
        file_name: str,
        repeat: bool = True
) -> None:
    await _get_user(user_id)

    Users.update(
        file=file_name,
        repeat=repeat
    ).where(
        Users.user_id == user_id
    ).execute()


@conn.atomic()
async def get_files_sending(repeat: bool = True) -> list[str] | None:
    users = Users.select(
        Users.file
    ).where(
        Users.file != None,  # noqa
        Users.repeat == repeat
    ).group_by(
        Users.file
    )

    if users.count() > 0:
        return list(x.file for x in users)

    return []


@conn.atomic()
async def reset_repeat():
    Users.update(
        repeat=False
    ).execute()


def _settings_get_value(type_value, value):
    decoder = {
        'bool': lambda x: json.loads(x),
        'text': lambda x: x
    }
    return decoder.get(type_value, lambda x: x)(value)


def _settings_set_value(type_value, value):
    encoder = {
        'bool': lambda x: json.dumps(x),
        'text': lambda x: x
    }
    return encoder.get(type_value, lambda x: x)(value)


@conn.atomic()
async def get_settings():
    settings = Settings.select()
    if settings.count() > 0:
        return {
            x.name: {
                'type': x.type,
                'view_name': x.view_name,
                'value': _settings_get_value(x.type, x.value)
            }
            for x in settings
        }


@conn.atomic()
async def set_settings_value(key, value, type_value):
    Settings.update(
        value=_settings_set_value(type_value, value)
    ).where(
        Settings.name == key
    ).execute()


@conn.atomic()
async def get_users():
    users = Users.select()
    if users.count() > 0:
        return users
