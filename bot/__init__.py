async def init_commands():
    from bot import event_checker

    await event_checker.load_storage()
