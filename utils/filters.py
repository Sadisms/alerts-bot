from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS_IDS, BOT_CONFIG


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message) -> bool:
        return message.from_user.id.__str__() in ADMINS_IDS


class ChannelFilter(BoundFilter):
    key = 'is_channel'

    def __init__(self, is_channel):
        self.is_channel = is_channel

    async def check(self, message: types.Message) -> bool:
        # return message.chat.id.__str__() == BOT_CONFIG['channel']
        return True
