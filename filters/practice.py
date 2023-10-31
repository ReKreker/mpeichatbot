from aiogram.filters import BaseFilter
from aiogram.types import Message


class FilesFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.photo is not None or message.document is not None
