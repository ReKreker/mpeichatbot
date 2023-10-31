from typing import Any

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

from data.cb_data import EventCbFactory, ButtonCbFactory, ButtonInfo
from data.database import Database

db = Database()


async def approve(query: types.CallbackQuery, state: FSMContext, bot: Bot) -> Any:
    await state.clear()
    await query.message.delete_reply_markup(query.inline_message_id)

    data = EventCbFactory.unpack(query.data)
    button = ButtonCbFactory.unpack(data.button)
    msg = ""
    if button.button == ButtonInfo.YES:
        msg = "Добавление баллов!"

        await db.connect()
        await db.new_user_event(query.from_user.id, button.id)
        await db.disconnect()

    else:
        msg = "С пруфами что-то не так.. Отпиши @rekreker"
    await bot.send_message(data.user_id, msg, reply_to_message_id=data.reply_msg_id)
    return await bot.answer_callback_query(callback_query_id=query.id)


async def add_event(msg: types.Message) -> Any:
    text = msg.text[10:]
    data = text.split("|")
    if len(data) != 2 or data[0].strip() == "" or data[1].strip() == "":
        await msg.reply("Введи <code>/add_event Название|Описание</code>")
        return

    name = data[0].strip()
    desc = data[1].strip()

    await db.connect()
    await db.new_event(name, desc)
    await db.disconnect()

    await msg.reply(f"'{name}' успешно создано")


async def del_event(msg: types.Message) -> Any:
    text = msg.text[10:]
    if text.strip() == "":
        await msg.reply("Введи <code>/del_event Название</code>")
        return

    name = text.strip()

    await db.connect()
    await db.del_event_by_name(name)
    await db.disconnect()

    await msg.reply(f"'{name}' успешно удалено")
