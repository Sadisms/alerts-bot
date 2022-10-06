import os
from pathlib import Path

from prettytable import PrettyTable

from data.config import FILE_CONFIG
from utils.dbworker import reset_repeat, get_settings, get_files_sending
from utils.logging import bot_log


def get_files() -> list[str]:
    Path(FILE_CONFIG['path']).mkdir(parents=True, exist_ok=True)
    return next(os.walk(FILE_CONFIG['path']), (None, None, []))[2]


def _file_path(f):
    return FILE_CONFIG['path'] + f"/{f}"


def get_files_data(
        files: list[str],
        skip_files: list[str] = None
):
    if skip_files is None:
        skip_files = []

    for f in files:
        if f not in skip_files:
            return f, open(_file_path(f), 'rb')


async def get_file_text(
        skip_files: list[str] | None
):
    settings = await get_settings()
    if not (files := get_files()):
        bot_log.warning('Not found files in directory!')
        return

    if files.sort() == skip_files.sort():
        if not settings['repeat']['value']:
            bot_log.warning('There are no more files for users!')
            return

        await reset_repeat()

        return get_files_data(
            files=files
        )

    return get_files_data(
        files=files,
        skip_files=skip_files
    )


async def add_file(file_name: str, content: bytes):
    Path(FILE_CONFIG['path']).mkdir(parents=True, exist_ok=True)

    with open(_file_path(file_name), 'wb') as f:
        f.write(content)


async def get_files_answer():
    if files := get_files():
        sent_files = await get_files_sending()
        table = PrettyTable()
        table.field_names = ["ID", "FILE NAME", "SENT"]
        for i, f in enumerate(files):
            table.add_row([i+1, f, f in sent_files])

        return f"<pre>{table.__str__()}</pre>"


def get_files_dict():
    files_list = {}
    if files := get_files():
        for i, f in enumerate(files):
            files_list[i+1] = f

    return files_list


def delete_file(file_name):
    if file_name in get_files():
        os.remove(_file_path(file_name))
