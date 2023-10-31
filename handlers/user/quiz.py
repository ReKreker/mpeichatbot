from aiogram import Bot
from aiogram import html, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import config
from data.cb_data import QuizCbFactory, ButtonCbFactory, ButtonInfo


async def gen_menu(msg: types.Message, bot: Bot) -> None:
    if msg.from_user is None:
        return

    await msg.reply("Отправлено на проверку")

    m = f"<a href='tg://user?id={msg.from_user.id}'>{html.quote(msg.from_user.full_name)}</a> победитель квиза?"

    kb = InlineKeyboardBuilder()
    no_button = QuizCbFactory(
        user_id=msg.from_user.id,
        reply_msg_id=msg.message_id,
        button=ButtonCbFactory(
            button=ButtonInfo.NO
        ).pack()
    ).pack()
    kb.add(
        types.InlineKeyboardButton(
            text="🚫",
            callback_data=no_button
        ))

    yes_button = QuizCbFactory(
        user_id=msg.from_user.id,
        reply_msg_id=msg.message_id,
        button=ButtonCbFactory(
            button=ButtonInfo.YES
        ).pack()
    ).pack()
    kb.add(
        types.InlineKeyboardButton(
            text="✅",
            callback_data=yes_button
        ))
    kb.adjust(2)

    for i in config.ADMINS:
        await bot.send_message(i, m, reply_markup=kb.as_markup())

    for i in config.TO_NOTIF:
        await bot.send_message(i, m, reply_markup=None)
