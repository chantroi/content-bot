import os
import requests


secret = requests.get(os.getenv("SECRET"), timeout=99)
res = secret.json()
dapi = res["api"]["content"]["td"]
bot_token: str = res["discord"]["content"]
tg_token = res["telegram"]["bot"]["douyin"]
google_api = res["key"]["google_ai"]
