import discord

class Basic:
    def __init__(self, bot):
        self.bot = bot
    @self.bot.slash_command()
    async def content(self, ctx):
        await ctx.respond("Đây là Content Download phiên bản Discord")
    
def setup(bot):
    bot.add_cog(Basic(bot))