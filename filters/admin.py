from __future__ import annotations

from aiogram.filters import BaseFilter
from aiogram.types import Message

from data import config


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in config.ADMINS
