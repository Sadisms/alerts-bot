import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_dialog import DialogRegistry

from data.config import BOT_CONFIG
from utils.filters import AdminFilter, ChannelFilter
from utils.logging import create_logger

bot = Bot(
    token=BOT_CONFIG['token'],
    parse_mode=ParseMode.HTML
)

storage = MemoryStorage()
dp = Dispatcher(
    bot=bot,
    storage=storage
)

registry = DialogRegistry(dp)

logging_md = LoggingMiddleware()
logging_md.logger = create_logger('requests', 'telegram_request')

dp.middleware.setup(logging_md)

dp.filters_factory.bind(AdminFilter)
dp.filters_factory.bind(ChannelFilter)

loop = asyncio.get_event_loop()

