from environs import Env

import os

os.environ['ADMINS'] = "848438079"
os.environ['TO_NOTIF'] = "848438079"
os.environ['BOT_TOKEN'] = "6036111995:AAFnqTm4Llx3xrMaL5NlDwwP-P_izRqzFpM"
os.environ['PG_HOST'] = "localhost"
os.environ['PG_PORT'] = "5432"
os.environ['PG_USER'] = "postgres"
os.environ['PG_HOST'] = "localhost"
os.environ['PG_PASSWORD'] = "postgres"
os.environ['PG_DATABASE'] = "mpeichatbot"

env = Env()
env.read_env()

ADMINS: list[int] = [int(i) for i in env.str("ADMINS").split("|")]  # на текущий момент может быть лишь один админ,
# потому что только один человек должен валидиловать выдачу баллов. Если это будут делать двое, то неибежен двойной
# инкремент, ибо нет проверки на то, провалидировал ли уже второй админ
TO_NOTIF: list[int] = [int(i) for i in env.str("TO_NOTIF").split("|") if i != ""]

BOT_TOKEN: str = env.str("BOT_TOKEN")
LOGGING_LEVEL: int = env.int("LOGGING_LEVEL", 10)

PG_HOST: str = env.str("PG_HOST")
PG_PORT: int = env.int("PG_PORT")
PG_USER: str = env.str("PG_USER")
PG_PASSWORD: str = env.str("PG_PASSWORD")
PG_DATABASE: str = env.str("PG_DATABASE")
