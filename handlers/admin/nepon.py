from typing import Any

from aiogram import types, Bot

from data.cb_data import NeponCbFactory


async def approve(query: types.CallbackQuery, bot: Bot) -> Any:
    await query.message.delete_reply_markup(query.inline_message_id)

    data = NeponCbFactory.unpack(query.data)
    await bot.send_message(data.user_id, "Добавление баллов!", reply_to_message_id=data.reply_msg_id)
    # TODO: добавление баллов в SQL
    return await bot.answer_callback_query(callback_query_id=query.id)
