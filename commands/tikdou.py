from discord.ext import commands
import discord
import requests
import os
import re

dapi = os.getenv("DAPI")

class TTDY(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ttdy(self, ctx):
        await ctx.trigger_typing()
        url = re.search(r"(?P<url>https?://[^\s]+)", ctx.message.content).group("url")
        r = requests.get(dapi + "/tikdou", params={"url": url}).json()
        dl_link = r.get("url")
        if isinstance(dl_link, list):
            for link in dl_link:
                await ctx.send(file=discord.File(link))
        else:
            await ctx.send(file=discord.File(dl_link))
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(TTDY(bot))