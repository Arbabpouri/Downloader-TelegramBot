from .Config import Config
from telethon import TelegramClient

try:
    client = TelegramClient(
        session= Config.SESSION_NAME,
        api_id= Config.API_ID,
        api_hash= Config.API_HASH,
    ).start(
        bot_token= Config.BOT_TOKEN,
    )
except Exception as ex:
    print(ex)