from discord.ext import commands
from environ import dapi, tg_token
import requests, re, io, discord

def tg_send(original, link):
    BUTTONS = [
    {"text": "Original", "url": original},
    {"text": "Youtube", "url": "https://youtube.com/@tiktokdouyin-share"},
    {"text": "Channel", "url": "https://t.me/contentdownload"},
    ]
    KEYBOARD = {"inline_keyboard": [BUTTONS]}
    VIDEO = {"chat_id": "contentdownload", "video": link, "reply_markup": KEYBOARD, "caption": "_*Discord Cross-Platform*_"}
    URL = f"https://api.telegram.org/bot{tg_token}/sendVideo?chat_id=contentdownload"
    response = requests.post(URL, json=VIDEO)
    print(response.json())

class TTDy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if any(match in message.content for match in ["tiktok", "douyin"]):
            await message.channel.trigger_typing()
            url = re.search(r"(?P<url>https?://[^\s]+)", message.content).group("url")
            r = requests.get(dapi + "/tikdou", params={"url": url}).json()
            dl_link = r.get("url")
            if isinstance(dl_link, list):
                for link in dl_link:
                    bytes_data = requests.get(link).content
                    file = io.BytesIO(bytes_data)
                    file.name = "image.jpg"
                    await message.channel.send(file=discord.File(file))
            else:
                bytes_data = requests.get(dl_link).content
                file = io.BytesIO(bytes_data)
                file.name = "video.mp4"
                await message.channel.send(file=discord.File(file))
                if message.channel == self.bot.get_channel(1095488012638507028):
                    #req = requests.post(f"https://api.telegram.org/bot{tg_token}/sendMessage", params={"chat_id": -1001559828576, "text": url})
                    #print(req.text)
                    tg_send(url, dl_link)
                    await message.delete()
            
def setup(bot):
    bot.add_cog(TTDy(bot))