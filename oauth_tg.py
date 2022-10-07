from pyrogram import Client

from data.config import PYROGRAM_CONFIG

client = Client('app', **PYROGRAM_CONFIG)
client.start()