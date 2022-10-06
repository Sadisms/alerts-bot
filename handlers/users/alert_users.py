from aiogram import types
from pyrogram import Client

from data.config import PYROGRAM_CONFIG
from loader import dp
from utils.dbworker import get_files_sending, add_user, get_settings
from utils.files_helper import get_file_text
from utils.logging import bot_log


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS, is_channel=True)
async def alert_for_new_users(message: types.Message):
    user_id = message.values['new_chat_participant']['id']
    settings = await get_settings()

    bot_log.info(f'New user: {user_id} in group')

    async with Client("app", **PYROGRAM_CONFIG) as app:
        await app.send_message(
            chat_id=user_id,
            text=settings['wellcome_message']['value']
        )

    if file_data := await get_file_text(
        skip_files=await get_files_sending()
    ):
        file_name, file_data = file_data
        async with Client("app", **PYROGRAM_CONFIG) as app:
            await app.send_document(
                chat_id=user_id,
                document=file_data,
                file_name=file_name
            )

        bot_log.info(f'Send file: {file_name} to user {user_id}')

        await add_user(
            user_id=user_id,
            file_name=file_name
        )
