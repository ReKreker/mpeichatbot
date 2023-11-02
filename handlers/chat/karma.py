from typing import Any

from aiogram import types, Bot

from data import config
from data.database import Database

db = Database()


async def call(msg: types.Message, bot: Bot) -> Any:
    reply = msg.reply_to_message
    # TODO: тут может случится косяк, если добавить бота на чат-форум
    if reply is None:
        await msg.answer("Не могу без реплая добавить баллов за помощь", disable_notification=True)
        return

    # Борьба с самореплаем
    if msg.from_user.id == reply.from_user.id:
        await msg.answer("Так-с... Что это тут у нас? Реплай на своё сообщение, чтобы накрутить баллы? ＼（〇_ｏ）／",
                         disable_notification=True)
        return

    await db.connect()
    user_id = msg.from_user.id
    if not await db.get_user(user_id):
        await db.new_user(user_id, msg.from_user.full_name)
    await db.execute_query("UPDATE member SET karmas=karmas+1 WHERE user_id=$1", user_id)
    await db.disconnect()

    reply_id = msg.reply_to_message.message_id
    chat_id = msg.chat.id
    await bot.send_message(chat_id, "Добавление баллов за помощь другому участнику!",
                           reply_to_message_id=reply_id, disable_notification=True)

    for i in config.ADMINS:
        await bot.send_message(i, f"<a href='{reply.from_user.url}'>{reply.from_user.full_name}</a> помог" + \
                               f" <a href='{msg.from_user.url}'>{msg.from_user.full_name}</a>!")
