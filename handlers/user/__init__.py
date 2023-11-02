from aiogram import Router
from aiogram.filters import CommandStart, Command, and_f, StateFilter

from filters import ChatTypeFilter, ContentFilter
from states.user import Practice, Event
from utils import media
from . import start, event, nepon, quiz, practice


def prepare_router() -> Router:
    router = Router()
    router.message.filter(ChatTypeFilter("private"))
    # start command handler
    start_route = Router()
    start_route.message.register(start.start, CommandStart())
    router.include_router(start_route)
    # help command handler
    help_route = Router()
    help_route.message.register(start.help_msg, Command("help"))
    router.include_router(help_route)
    # Nepon
    nepon_route = Router()
    nepon_route.message.register(nepon.gen_menu, Command("nepon"))
    router.include_router(nepon_route)
    # Quizwinner
    quiz_route = Router()
    quiz_route.message.register(quiz.gen_menu, Command("quizwinner"))
    router.include_router(quiz_route)

    # Practice
    pract_route = Router()
    pract_route.message.register(practice.gen_menu, Command("practice"))
    router.include_router(pract_route)
    # Require practice's proofs
    pract_req_route = Router()
    pract_req_route.callback_query.filter(Practice.generated)
    pract_req_route.callback_query.register(practice.require_proofs)
    router.include_router(pract_req_route)
    # Get practice's proofs
    pract_proof_route = Router()
    pract_proof_route.message.filter(and_f(
        StateFilter(Practice.getting_proofs),
        ContentFilter()
    ))
    pract_proof_route.message.register(media.proof_handler)
    router.include_router(pract_proof_route)
    # Get next proof
    practice_nproof_route = Router()
    practice_nproof_route.message.filter(and_f(
        StateFilter(Practice.next_proof),
        ContentFilter()
    ))
    practice_nproof_route.message.register(media.next_proof_handler)
    router.include_router(practice_nproof_route)
    # Forward proofs
    practice_forward_route = Router()
    practice_forward_route.message.filter(StateFilter(Practice.next_proof))
    practice_forward_route.message.register(media.forward)
    router.include_router(practice_forward_route)

    # Event
    event_route = Router()
    event_route.message.register(event.gen_menu, Command("event"))
    router.include_router(event_route)
    # Require event's proofs
    event_req_route = Router()
    event_req_route.callback_query.filter(Event.generated)
    event_req_route.callback_query.register(event.require_proofs)
    router.include_router(event_req_route)
    # Get event's proofs
    event_proof_route = Router()
    event_proof_route.message.filter(and_f(
        StateFilter(Event.getting_proofs),
        ContentFilter()
    ))
    event_proof_route.message.register(media.proof_handler)
    router.include_router(event_proof_route)
    # Get next proof
    event_nproof_route = Router()
    event_nproof_route.message.filter(and_f(
        StateFilter(Event.next_proof),
        ContentFilter()
    ))
    event_nproof_route.message.register(media.next_proof_handler)
    router.include_router(event_nproof_route)
    # Forward proofs
    event_forward_route = Router()
    event_forward_route.message.filter(StateFilter(Event.next_proof))
    event_forward_route.message.register(media.forward)
    router.include_router(event_forward_route)

    return router
