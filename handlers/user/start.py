from aiogram import html, types


async def start(msg: types.Message):
    if msg.from_user is None:
        return
    m = [
        f'Привет, {html.quote(msg.from_user.full_name)}!',
        'Это бот, который будет подсчитывать баллы за факультатив',
        'Пока он находится в разработке, так что буду рад фидбеку в <a href="tg://user?id=1309263872">лс</a>',
        '',
        'Нажми /help, чтобы узнать команды бота',
    ]
    await msg.answer("\n".join(m))
    # TODO: если пользователя не существует в БД, то создать


async def help_msg(msg: types.Message):
    if msg.from_user is None:
        return
    m = [
        '/nepon {термин} - попросить спикера объяснить использованный термин',
        '/quizwinner - накинуть баллов за выигрыш в квизе'
        '/practice - сдать практику'
        '/event - сдать мероприятие'
    ]
    await msg.answer("\n".join(m))
