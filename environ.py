from types import SimpleNamespace
from deta import Deta
import os, requests, json

def res():
    secret = requests.get(os.getenv("SECRET")).text
    return json.loads(secret, object_hook=lambda _: SimpleNamespace(**_))
    
res = res()
#deta = Deta(res.key.web_collection)
bot_token = res.bot.discord
tg_token = res.bot.td_tg