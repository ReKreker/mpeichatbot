from typing import Any

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.methods import AnswerCallbackQuery

from data.cb_data import QuizCbFactory


async def approve(query: types.CallbackQuery, state: FSMContext, bot: Bot) -> Any:
    await state.clear()
    await query.message.delete_reply_markup(query.inline_message_id)

    data = QuizCbFactory.unpack(query.data)
    msg = ""
    if data.is_yes:
        msg = "Добавление баллов!"
        # TODO: добавление баллов в SQL
    else:
        msg = "Выглядит так, будто ты не побеждал в квизе🤔"
    await bot.send_message(data.user_id, msg, reply_to_message_id=data.reply_msg_id)
    return await bot(AnswerCallbackQuery(callback_query_id=query.id))
