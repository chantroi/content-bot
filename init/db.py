from deta import Deta
import os

deta = Deta(os.getenv("DETA_KEY"))
base = deta.Base("tokens")
bot_token = base.get("discord")["token"]
tg_token = base.get("bot")["td"]