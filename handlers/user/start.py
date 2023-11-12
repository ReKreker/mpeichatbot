from aiogram import html, types

from data.database import Database

db = Database()


async def start(msg: types.Message):
    if msg.from_user is None:
        return

    await db.connect()
    if not await db.get_user(msg.from_user.id):
        await db.new_user(msg.from_user.id, msg.from_user.full_name)
    await db.disconnect()

    m = [
        f'Привет, {html.quote(msg.from_user.full_name)}!',
        'Это бот, который будет подсчитывать баллы за факультатив кружка CTF',
        'Пока он находится в разработке, так что буду рад фидбеку в <a href="tg://user?id=1309263872">лс</a>',
        '',
        'Нажми /help, чтобы узнать команды бота',
    ]
    await msg.answer("\n".join(m))


async def help_msg(msg: types.Message):
    if msg.from_user is None:
        return
    m = [
        '/nepon {термин} - попросить спикера объяснить использованный термин',
        '/quizwinner - накинуть баллов за выигрыш в квизе',
        '/practice - сдать практику',
        '/event - сдать мероприятие',
    ]
    await msg.answer("\n".join(m))
