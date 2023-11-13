from typing import Any

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

from data import config
from data.cb_data import EventCbFactory, ButtonCbFactory, ButtonInfo
from data.database import Database
from utils.db_processing import mark_as_done, fully_del_x

db = Database("event")


async def approve(query: types.CallbackQuery, state: FSMContext, bot: Bot) -> bool:
    await query.message.delete_reply_markup(query.inline_message_id)

    data = EventCbFactory.unpack(query.data)
    button = ButtonCbFactory.unpack(data.button)
    if button.button == ButtonInfo.NO:
        msg = "Не принятo"
    else:
        await db.connect()
        msg = await mark_as_done(db, data.user_id, button.id)
        await db.disconnect()

    await bot.send_message(data.user_id, msg, reply_to_message_id=data.reply_msg_id)
    for i in config.ADMINS:
        await bot.send_message(i, msg)
    return await bot.answer_callback_query(callback_query_id=query.id)


async def add_event(msg: types.Message) -> Any:
    cmd_len = msg.entities[0].length + 1
    text = msg.text[cmd_len:]

    name_end, desc_beg = text.find("|"), msg.html_text.find("|") + 1
    name, desc = text[:name_end], msg.html_text[desc_beg:]

    if name.strip() == "" or desc.strip() == "":
        await msg.reply("Введи <code>/add_event Название|Описание</code>")
        return

    await db.connect()
    await db.new_x(name, desc)
    await db.disconnect()

    await msg.reply(f"'{name}' успешно создано")


async def del_event(msg: types.Message) -> Any:
    cmd_len = msg.entities[0].length + 1
    text = msg.text[cmd_len:]
    name = text.strip()

    if name == "":
        await msg.reply("Введи <code>/del_event Название</code>")
        return

    await db.connect()
    ret_msg = await fully_del_x(db, name)
    await db.disconnect()

    await msg.reply(ret_msg)
