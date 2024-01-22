import discord
from discord.ext import commands

class Basic:
    @commands.slash_command()
    async def content(ctx):
        await ctx.respond("Đây là Content Download phiên bản Discord")
    
def setup(bot):
    bot.add_cog(Basic())