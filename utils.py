import pickle
import os.path

from typing import Generic, TypeVar
from logging import getLogger, INFO
from asyncio import get_running_loop, Lock
from traceback import format_exc


logger = getLogger('bot')
logger.setLevel(INFO)


STORAGE_DIR = os.path.join(os.path.dirname(__file__), 'storage')

_DataType = TypeVar('_DataType')


class Storage(Generic[_DataType]):
    path: str
    data: _DataType
    flush_lock: Lock

    def __init__(self, filename: str, default: _DataType) -> None:
        self.path = os.path.join(STORAGE_DIR, filename)
        self.flush_lock = Lock()

        try:
            with open(self.path, 'rb') as file:
                self.data = pickle.load(file)
        except Exception:
            logger.warning('Не удалось загрузить данные из хранилища '
                          f'"{filename}", установлено значение по умолчанию:\n'
                          f'{format_exc()}')
            self.data = default

    def _flush_sync(self):
        with open(self.path, 'wb') as file:
            pickle.dump(self.data, file)

    async def flush(self):
        loop = get_running_loop()
        async with self.flush_lock:
            await loop.run_in_executor(None, self._flush_sync)
