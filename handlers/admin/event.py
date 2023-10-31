from typing import Any

from aiogram import types, Bot
from aiogram.methods import AnswerCallbackQuery

from data.cb_data import EventChooseCbFactory
from data.database import Database


async def approve(query: types.CallbackQuery, bot: Bot, db: Database) -> Any:
    await query.message.delete_reply_markup(query.inline_message_id)
    data = EventChooseCbFactory.unpack(query.data)
    msg = ""
    if data.is_yes:
        msg = "Добавление баллов!"
        # TODO: добавление баллов в SQL
    else:
        msg = "С пруфами что-то не так.. Отпиши @rekreker"
    await bot.send_message(data.user_id, msg, reply_to_message_id=data.reply_msg_id)
    return await bot(AnswerCallbackQuery(callback_query_id=query.id))


async def add_event(msg: types.Message, db: Database) -> Any:
    text = msg.text[10:]
    data = text.split("|")
    if len(data) != 2 or data[0].strip() == "" or data[1].strip() == "":
        await msg.reply("Введи <code>/add_event Название|Описание</code>")
        return

    name = data[0].strip()
    desc = data[1].strip()
    db.new_event()
    await msg.reply(f"'{name}' успешно создано")


async def del_event(msg: types.Message) -> Any:
    text = msg.text[10:]
    if text.strip() == "":
        await msg.reply("Введи <code>/del_event Название</code>")
        return

    name = text.strip()
    # TODO: добавить удаление мероприятия в SQL
    await msg.reply(f"'{name}' успешно удалено")
