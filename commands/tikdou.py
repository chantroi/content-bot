from discord import Cog
import discord
import requests
import os

dapi = os.getenv("DAPI")

class TTDY(Cog):
    def __init__(self, bot):
        self.bot = bot
    @Cog.listen()
    async def tikdou(self, ctx):
        await ctx.typing()
        url = re.search(r"(?P<url>https?://[^\s]+)", ctx.content).group("url")
        r = requests.get(dapi = "/tikdou", params={"url": url}).json()
        dl_link = r.get("url")
        if isinstance(dl_link, list):
            for link in dl_link:
                await ctx.respond(file=discord.File(link))
        else:
            await ctx.respond(file=discord.File(dl_link))
        await ctx.delete()
    
def setup(bot):
    bot.add_cog(TTDY(bot))