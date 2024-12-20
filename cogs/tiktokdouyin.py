from typing import Dict, List, Optional, Union

import requests
import re
import io
import discord
from discord.ext import commands
from env_config import dapi, tg_token


class TiktokDouyin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if any(match in message.content for match in ["tiktok", "douyin"]):
            await message.channel.trigger_typing()
            url_match: Optional[re.Match] = re.search(
                r"(?P<url>https?://[^\s]+)", message.content)
            if not url_match:
                return
            url: str = url_match.group("url")

            r: Dict = requests.get(dapi, params={"url": url}, timeout=99).json()
            dl_link: Union[str, List[str]] = r.get("url")
            if isinstance(dl_link, list):
                for link in dl_link:
                    bytes_data: bytes = requests.get(link, timeout=99).content
                    file: io.BytesIO = io.BytesIO(bytes_data)
                    file.name = "image.jpg"
                    await message.channel.send(file=discord.File(file))
            else:
                bytes_data: bytes = requests.get(dl_link, timeout=99).content
                file: io.BytesIO = io.BytesIO(bytes_data)
                file.name = "video.mp4"
                await message.channel.send(file=discord.File(file))
                if message.channel == self.bot.get_channel(1095488012638507028):
                    req: requests.Response = requests.post(
                        f"https://api.telegram.org/bot{tg_token}/sendMessage",
                        params={"chat_id": -1001559828576, "text": url},
                        timeout=99,
                    )
                    print(req.text)
                    await message.delete()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(TiktokDouyin(bot))
