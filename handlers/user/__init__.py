from aiogram import Router
from aiogram.filters import CommandStart, Command

import states
from data import cb_data
from filters import ChatTypeFilter, PracticeFilesFilter
from . import start, nepon, quiz, practice


def prepare_router() -> Router:
    router = Router()
    # >
    chats_route = Router()
    chats_route.message.filter(ChatTypeFilter("private"))
    # >>
    start_route = Router()
    start_route.message.register(start.start, CommandStart())
    chats_route.include_router(start_route)
    # >>
    help_route = Router()
    help_route.message.register(start.help_msg, Command("help"))
    chats_route.include_router(help_route)
    # >>
    nepon_route = Router()
    nepon_route.message.register(nepon.call, Command("nepon"))
    chats_route.include_router(nepon_route)
    # >>
    quiz_route = Router()
    quiz_route.message.register(quiz.call, Command("quizwinner"))
    chats_route.include_router(quiz_route)
    # >>
    pract_list_route = Router()
    pract_list_route.message.register(practice.get_pract_name, Command("practice"))
    chats_route.include_router(pract_list_route)
    # >>
    pract_route = Router()
    pract_route.callback_query.filter(cb_data.PractListCbFactory.filter())
    pract_route.callback_query.register(practice.send_info)
    chats_route.include_router(pract_route)
    # >>
    pract_forward_route = Router()
    pract_forward_route.message.filter(states.user.Event.to_upload)
    pract_forward_route.message.filter(PracticeFilesFilter())
    pract_forward_route.message.register(practice.forward)
    chats_route.include_router(pract_forward_route)
    # >
    router.include_router(chats_route)

    return router
