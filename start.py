# Главное оправдание всем "плохим" решениям -- это было написано в 3 часа ночи

if __name__ == '__main__':
    import asyncio

    from traceback import format_exc

    from utils import logger


    async def run_bot():
        from bot.client import create_client

        await create_client()

        from bot import init_commands

        await init_commands()

        from bot.client import user_client


        while True:
            try:
                await user_client.run_until_disconnected()  # type: ignore
            except Exception:
                logger.error('Произошла ошибка при '
                            f'получении событий:\n{format_exc()}')
            await asyncio.sleep(30)


    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print()
        print('Завершение...')
