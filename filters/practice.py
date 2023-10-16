from aiogram.filters import BaseFilter
from aiogram.types import Message


class PracticeFilesFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return (message.photo is not None and 0 < len(message.photo) < 2) or message.document is not None
