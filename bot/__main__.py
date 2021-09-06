import os
import sys
import asyncio
from pyrogram import Client, idle
from config import Config
ADMINS = Config.ADMINS
USERNAME = Config.BOT_USERNAME
REPLY_MESSAGE = Config.REPLY_MESSAGE

User = Client(
    Config.SESSION_STRING,
    Config.API_ID,
    Config.API_HASH
)

Bot = Client(
    ":memory:",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="bot.safone"),
)
if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")

Bot.start()
User.start()
print("\nVideo Player Bot Started!")

idle()
Bot.stop()
User.stop()
print("\nVideo Player Bot Stopped!")
