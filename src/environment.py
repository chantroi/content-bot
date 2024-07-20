import os
import requests


secret = requests.get(os.getenv("SECRET"), timeout=99)
res = secret.json()
dapi = res['api']['dapi']['tiktokdouyin']
bot_token = res['bot']['contentdiscord']
tg_token = res['bot']['tiktokdouyin']
google_api = res['api']['google_ai']
