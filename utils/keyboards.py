from __future__ import annotations

from aiogram.types import Message, InlineKeyboardButton

from data.cb_data import *


class BuildKb:

    def __init__(self, cb_factory, msg: Message) -> None:
        self.cb_factory = cb_factory
        self.msg = msg

    def get_button(self, text: str, button_id: ButtonInfo, ident: int):
        cb_info = self.cb_factory(
            user_id=self.msg.from_user.id,
            reply_msg_id=self.msg.message_id,
            button=ButtonCbFactory(
                id=ident,
                button=button_id
            ).pack()
        ).pack()
        return InlineKeyboardButton(
            text=text,
            callback_data=cb_info
        )
