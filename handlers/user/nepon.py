from aiogram import Bot
from aiogram import html, types
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import config
from data.cb_data import NeponCbFactory


async def call(msg: types.Message, bot: Bot) -> None:
    if msg.from_user is None:
        return
    if msg.text.strip() == "/nepon":
        nepon_without_term = FSInputFile("memes/nepon_without_term.png")
        await msg.reply_photo(nepon_without_term)
        return

    await msg.reply("Отправлено спикеру!")

    m = [
        f"От <a href='tg://user?id={msg.from_user.id}'>{html.quote(msg.from_user.full_name)}</a> пришёл непон:",
        msg.text[6:].strip()
    ]

    # TODO: добавить 1-ти дневный таймаут на отображение этой кнопки для админа
    data = NeponCbFactory(user_id=msg.from_user.id, reply_msg_id=msg.message_id)
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="✅",
            callback_data=data.pack()
        ))
    markup = builder.as_markup()

    for i in config.ADMINS:
        await bot.send_message(i, "\n".join(m), reply_markup=markup)

    for i in config.TO_NOTIF:
        await bot.send_message(i, "\n".join(m), reply_markup=None)
