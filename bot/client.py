from telethon import TelegramClient

import config


user_client: TelegramClient


async def create_client():
    global user_client

    client = TelegramClient('main', config.app_id, config.api_hash)
    user_client = await client.start(config.phone_number)  # type: ignore


# async def close_client():
#     user_client.close
