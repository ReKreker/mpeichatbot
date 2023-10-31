from aiogram import Router
from aiogram.filters import Command, and_f

import states
from data import cb_data
from filters import ChatTypeFilter, AdminFilter
from . import nepon, quiz, practice, event


def prepare_router() -> Router:
    router = Router()
    router.message.filter(and_f(
        ChatTypeFilter("private"),
        AdminFilter()
    ))

    # Receive nepon
    nepon_route = Router()
    nepon_route.callback_query.filter(cb_data.NeponCbFactory.filter())
    nepon_route.callback_query.register(nepon.approve)
    router.include_router(nepon_route)

    # Receive quiz
    quiz_route = Router()
    quiz_route.callback_query.filter(cb_data.QuizCbFactory.filter())
    quiz_route.callback_query.register(quiz.approve)
    router.include_router(quiz_route)

    # Receive practice
    pract_route = Router()
    pract_route.callback_query.filter(and_f(
        cb_data.PractCbFactory.filter(),
        states.user.Activity.forwarded
    ))
    pract_route.callback_query.register(practice.approve)
    router.include_router(pract_route)
    # Add practice
    add_pract_route = Router()
    add_pract_route.message.register(practice.add_practice, Command("add_pract"))
    router.include_router(add_pract_route)
    # Del practice
    del_pract_route = Router()
    del_pract_route.message.register(practice.del_practice, Command("del_pract"))
    router.include_router(del_pract_route)

    # Receive event
    event_route = Router()
    event_route.callback_query.filter(and_f(
        cb_data.EventCbFactory.filter(),
        states.user.Activity.forwarded
    ))
    event_route.callback_query.register(event.approve)
    router.include_router(event_route)
    # Add event
    add_event_route = Router()
    add_event_route.message.register(event.add_event, Command("add_event"))
    router.include_router(add_event_route)
    # Del event
    del_event_route = Router()
    del_event_route.message.register(event.del_event, Command("del_event"))
    router.include_router(del_event_route)

    return router
