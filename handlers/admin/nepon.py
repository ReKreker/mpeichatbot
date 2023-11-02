from aiogram import types, Bot

from data.cb_data import NeponCbFactory
from data.database import Database

db = Database()


async def approve(query: types.CallbackQuery, bot: Bot) -> bool:
    await query.message.delete_reply_markup(query.inline_message_id)

    data = NeponCbFactory.unpack(query.data)

    # таймаут на 24 часа на отображение кнопки одобрения для запросов от конкретного юзера
    await db.connect()
    recent = await db.execute_query("SELECT * FROM nepon WHERE time >= CURRENT_TIMESTAMP - INTERVAL '24 hours'")
    if len(recent) == 0:
        await bot.send_message(data.user_id, "Добавление баллов!", reply_to_message_id=data.reply_msg_id)
        await db.insert_data("nepon", {"user_id": data.user_id})
    await db.disconnect()

    return await bot.answer_callback_query(callback_query_id=query.id)
