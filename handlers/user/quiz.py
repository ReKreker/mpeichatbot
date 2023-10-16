from aiogram import Bot
from aiogram import html, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import config
from data.cb_data import QuizCbFactory


async def call(msg: types.Message, bot: Bot) -> None:
    if msg.from_user is None:
        return

    await msg.reply("Отправлено на проверку")

    m = f"<a href='tg://user?id={msg.from_user.id}'>{html.quote(msg.from_user.full_name)}</a> победитель квиза?"

    builder = InlineKeyboardBuilder()
    no_data = QuizCbFactory(user_id=msg.from_user.id, reply_msg_id=msg.message_id, is_yes=False)
    builder.add(
        types.InlineKeyboardButton(
            text="🚫",
            callback_data=no_data.pack()
        ))
    yes_data = QuizCbFactory(user_id=msg.from_user.id, reply_msg_id=msg.message_id, is_yes=True)
    builder.add(
        types.InlineKeyboardButton(
            text="✅",
            callback_data=yes_data.pack()
        ))
    builder.adjust(2)
    markup = builder.as_markup()

    for i in config.ADMINS:
        await bot.send_message(i, "\n".join(m), reply_markup=markup)

    for i in config.TO_NOTIF:
        await bot.send_message(i, "\n".join(m), reply_markup=None)
