from typing import Any

from aiogram import types, Bot


async def call(msg: types.Message, bot: Bot) -> Any:
    reply_msg = msg.reply_to_message.reply_to_message
    if reply_msg is None or reply_msg.text == "":
        await msg.reply("Не могу без реплая добавить баллов за помощь", disable_notification=True)
        return

    # TODO: добавить увеличение баллов в SQL
    reply_id = msg.reply_to_message.message_id
    chat_id = msg.chat.id
    m = "Добавление баллов за помощь другому участнику!"
    await bot.send_message(text=m, chat_id=chat_id, reply_to_message_id=reply_id, disable_notification=True)
