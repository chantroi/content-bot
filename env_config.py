from typing import Dict, Any

import os
import requests


secret: requests.Response = requests.get(os.getenv("SECRET"), timeout=99)
res: Dict[str, Any] = secret.json()
dapi: str = res["api"]["content"]["td"]
bot_token: str = res["discord"]["content"]
tg_token: str = res["telegram"]["bot"]["douyin"]
google_api: str = res["key"]["google_ai"]
