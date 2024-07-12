import requests
import re
import io
import discord
from discord.ext import commands
from environment import dapi, tg_token


class TiktokDouyin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if any(match in message.content for match in ["tiktok", "douyin"]):
            await message.channel.trigger_typing()
            url = re.search(r"(?P<url>https?://[^\s]+)", message.content).group("url")
            r = requests.get(dapi + "/tikdou", params={"url": url}, timeout=99).json()
            dl_link = r.get("url")
            if isinstance(dl_link, list):
                for link in dl_link:
                    bytes_data = requests.get(link, timeout=99).content
                    file = io.BytesIO(bytes_data)
                    file.name = "image.jpg"
                    await message.channel.send(file=discord.File(file))
            else:
                bytes_data = requests.get(dl_link, timeout=99).content
                file = io.BytesIO(bytes_data)
                file.name = "video.mp4"
                await message.channel.send(file=discord.File(file))
                if message.channel == self.bot.get_channel(1095488012638507028):
                    req = requests.post(
                        f"https://api.telegram.org/bot{tg_token}/sendMessage",
                        params={"chat_id": -1001559828576, "text": url},
                        timeout=99,
                    )
                    print(req.text)
                    await message.delete()


def setup(bot):
    bot.add_cog(TiktokDouyin(bot))
