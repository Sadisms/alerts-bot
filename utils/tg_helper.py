import os
import zipfile
from io import BytesIO
from datetime import datetime

import pandas as pd
from aiogram import types

from data.config import PATH_LOGS
from utils.dbworker import get_users


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Начало работы с ботом"),
    ])


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def get_logs_archive():
    zip_archive = BytesIO()

    with zipfile.ZipFile(zip_archive, 'w') as z:
        zipdir(PATH_LOGS, z)

    zip_archive.seek(0)
    return types.InputFile(zip_archive, filename=f'logs_{datetime.now().strftime("%d-%m-%Y")}.zip')


async def get_excel_users():
    if users := await get_users():
        file = BytesIO()
        df = pd.DataFrame(list(users.dicts()))
        df.to_excel(file)
        file.seek(0)

        return types.InputFile(file, filename=f'users_{datetime.now().strftime("%d-%m-%Y")}.xlsx')