import os
import requests
import json
from types import SimpleNamespace

secret = requests.get(os.getenv("SECRET"), timeout=99).text
res = json.loads(secret, object_hook=lambda _: SimpleNamespace(**_))
dapi = res.api.dapi
bot_token = res.bot.discord
tg_token = res.bot.tiktokdouyin
