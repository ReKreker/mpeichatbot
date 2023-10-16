from aiogram import Bot
from aiogram import html, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import config
from data.cb_data import EventChooseCbFactory, EventListCbFactory
from states.user import Event


async def get_pract_name(msg: types.Message, state: FSMContext) -> None:
    if msg.from_user is None:
        return
    await state.clear()

    # TODO: извлекать из SQL названия всех мероприятий(желательно от недавних до поздних)
    test_names = ["Мероприятие 1", "Мероприятие 2", "Мероприятие 3"]
    practicies = InlineKeyboardBuilder()
    for i in range(len(test_names)):
        data = EventListCbFactory(user_id=msg.from_user.id, reply_msg_id=msg.message_id, name=test_names[i])
        practicies.add(types.InlineKeyboardButton(text=test_names[i], callback_data=data.pack()))
    practicies.adjust(1)
    await msg.reply("Выбери, какое мероприятие сдать:", reply_markup=practicies.as_markup())


async def send_info(query: types.CallbackQuery, state: FSMContext) -> None:
    await query.message.delete()
    await query.message.answer(
        "Вышли практику в предалах 1 картинки или 1 файла (предпочительно docx/pdf, но можно и zip)"
    )

    data = EventListCbFactory.unpack(query.data)
    await state.set_data({"name": data.name})
    await state.set_state(Event.to_upload)


async def forward(msg: types.Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    m = [
        f"<a href='tg://user?id={msg.from_user.id}'>{html.quote(msg.from_user.full_name)}</a> прислал практику!",
        data["name"]
    ]

    builder = InlineKeyboardBuilder()
    no_data = EventChooseCbFactory(user_id=msg.from_user.id, reply_msg_id=msg.message_id, is_yes=False)
    builder.add(
        types.InlineKeyboardButton(
            text="🚫",
            callback_data=no_data.pack()
        ))
    yes_data = EventChooseCbFactory(user_id=msg.from_user.id, reply_msg_id=msg.message_id, is_yes=True)
    builder.add(
        types.InlineKeyboardButton(
            text="✅",
            callback_data=yes_data.pack()
        ))
    builder.adjust(2)
    markup = builder.as_markup()

    for i in config.ADMINS:
        await bot.forward_message(i, msg.from_user.id, msg.message_id)
        await bot.send_message(i, "\n".join(m), reply_markup=markup)

    for i in config.TO_NOTIF:
        await bot.forward_message(i, msg.from_user.id, msg.message_id)
        await bot.send_message(i, "\n".join(m), reply_markup=None)

    await state.set_state(Event.forwarded)
