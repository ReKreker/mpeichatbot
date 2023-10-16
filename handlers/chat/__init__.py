from aiogram import Router
from aiogram.filters import or_f

from filters import ChatTypeFilter, TextFilter
from . import karma


def prepare_router() -> Router:
    router = Router()
    router.message.filter(or_f(ChatTypeFilter("group"), ChatTypeFilter("supergroup")))
    router.message.filter(TextFilter(["Спасибо",
                                      "спасибо",
                                      "Благодарю",
                                      "благодарю",
                                      "Пасябо",
                                      "пасябо",
                                      "Пасибо",
                                      "пасибо",
                                      "Пасяб",
                                      "пасяб",
                                      "Пасиб",
                                      "пасиб"])
                          )
    router.message.register(karma.call)
    return router
