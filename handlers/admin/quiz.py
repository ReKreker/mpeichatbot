from aiogram import types, Bot

from data.cb_data import QuizCbFactory, ButtonCbFactory, ButtonInfo
from data.database import Database

db = Database()


async def approve(query: types.CallbackQuery, bot: Bot) -> bool:
    await query.message.delete_reply_markup(query.inline_message_id)

    data = QuizCbFactory.unpack(query.data)
    button = ButtonCbFactory.unpack(data.button)
    if button.button == ButtonInfo.NO:
        msg = "Не принятo"
    else:
        msg = "Добавление баллов!"
        await db.connect()
        await db.insert_data("quiz", {"user_id": data.user_id})
        await db.disconnect()

    await bot.send_message(data.user_id, msg, reply_to_message_id=data.reply_msg_id)
    return await bot.answer_callback_query(callback_query_id=query.id)
