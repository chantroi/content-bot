import os
import requests


secret = requests.get(os.getenv("SECRET"), timeout=99)
res = secret.json()
dapi = res["api"]["dapi"]["td"]
bot_token = res["access"]["discord"]
tg_token = res["access"]["telegram"]["td"]
google_api = res["access"]["google_ai"]
