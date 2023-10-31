from __future__ import annotations

from aiogram.enums import ContentType
from aiogram.filters import BaseFilter
from aiogram.types import Message


class ContentFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.content_type in [ContentType.PHOTO, ContentType.VIDEO, ContentType.DOCUMENT]
