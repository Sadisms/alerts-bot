from aiogram.utils import executor

import loader
import handlers  # noqa
from dialogs.admin_panel import settings_dialog

from utils.logging import bot_log
from utils.tg_helper import set_default_commands


async def on_startup(dispatcher):
    bot_log.info('Bot startup')
    await set_default_commands(dispatcher)
    await settings_dialog()


async def on_shutdown(dispatcher):
    bot_log.info('Bot shutdown')

    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=loader.dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        loop=loader.loop
    )

