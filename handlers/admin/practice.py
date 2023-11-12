from typing import Any

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

from data import config
from data.cb_data import PractCbFactory, ButtonCbFactory, ButtonInfo
from data.database import Database
from utils.db_processing import mark_as_done, fully_del_x

db = Database("practice")


async def approve(query: types.CallbackQuery, state: FSMContext, bot: Bot) -> bool:
    await state.clear()
    await query.message.delete_reply_markup(query.inline_message_id)

    data = PractCbFactory.unpack(query.data)
    button = ButtonCbFactory.unpack(data.button)
    if button.button == ButtonInfo.NO:
        msg = "Не принятo"
    else:
        await db.connect()
        msg = await mark_as_done(db, query.from_user.id, button.id)
        await db.disconnect()

    await bot.send_message(data.user_id, msg, reply_to_message_id=data.reply_msg_id)
    for i in config.ADMINS:
        await bot.send_message(i, msg)
    return await bot.answer_callback_query(callback_query_id=query.id)


async def add_practice(msg: types.Message) -> Any:
    text = msg.text[10:]
    data = text.split("|")
    if len(data) != 2 or data[0].strip() == "" or data[1].strip() == "":
        await msg.reply("Введи <code>/add_pract Название|Описание</code>")
        return

    # TODO: Добавить уведомляшки
    # TODO: Добавить возможность хранить уже отформатированное описание
    name = data[0].strip()
    desc = data[1].strip()

    await db.connect()
    await db.new_x(name, desc)
    await db.disconnect()

    await msg.reply(f"'{name}' успешно создано")


async def del_practice(msg: types.Message) -> Any:
    text = msg.text[10:]
    if text.strip() == "":
        await msg.reply("Введи <code>/del_pract Название</code>")
        return

    name = text.strip()

    await db.connect()
    ret_msg = await fully_del_x(db, name)
    await db.disconnect()

    await msg.reply(ret_msg)
