from collections import deque

from telethon.events import NewMessage, MessageDeleted

from utils import Storage
from bot.client import user_client


bound_storage: Storage['set[int]']
users_storage: Storage['dict[int, dict]']
message_storage: Storage['deque[dict]']


async def load_storage():
    global bound_storage, users_storage, message_storage

    users_storage = Storage('users', {})
    bound_storage = Storage('bound_chats', set())
    message_storage = Storage('messages', deque(maxlen=200))


@user_client.on(
    NewMessage(outgoing=True, pattern='!bind_watcher')
)
async def bind(event: NewMessage.Event):
    if (chat_id := event.chat_id) is None:
        return await event.reply('No chat id')

    if chat_id in bound_storage.data:
        await event.reply('Already bound.')
    else:
        bound_storage.data.add(chat_id)
        await bound_storage.flush()
        await event.reply('Ok!')


@user_client.on(
    NewMessage(outgoing=True, pattern='!unbind_watcher')
)
async def unbind(event: NewMessage.Event):
    if (chat_id := event.chat_id) is None:
        return await event.reply('No chat id')

    if chat_id not in bound_storage.data:
        await event.reply('Not bound.')
    else:
        bound_storage.data.remove(chat_id)
        await bound_storage.flush()
        await event.reply('Ok!')


@user_client.on(
    NewMessage(incoming=True)
)
async def add_message(event: NewMessage.Event):
    if event.chat_id not in bound_storage.data:
        return

    message_storage.data.append(event.message.to_dict())
    await message_storage.flush()

    if (from_id := event.message.from_id) is None:
        return

    from_user_id = from_id.user_id

    if from_user_id not in users_storage.data:
        sender = await event.message.get_sender()
        users_storage.data[from_user_id] = sender.to_dict()
        await users_storage.flush()


@user_client.on(MessageDeleted())
async def show_deleted_message(event: MessageDeleted.Event):
    # Здесь, по-хорошему, надо сделать словарь или множество с
    # ID сообщений, чтобы не перебирать весь список каждый раз

    for message in message_storage.data:
        if message['id'] in event.deleted_ids:
            peer = message['peer_id']
            if peer['_'] != 'PeerChat':
                continue

            if not (text := message['message']):
                continue

            from_id = message['from_id']
            if not from_id or from_id['_'] != 'PeerUser':
                continue

            user = users_storage.data.get(from_id['user_id'])
            if user is None:
                continue

            username = user['username']

            await user_client.send_message(
                peer['chat_id'],
                f'__@{username}__ удалил:\n```{text}```'
            )
            return
