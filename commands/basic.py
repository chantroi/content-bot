import discord

basic = discord.SlashCommand()

@basic.command()
async def content(ctx):
    await ctx.respond("Đây là Content Download phiên bản Discord")
    
def setup(bot):
    bot.add_application_command(basic)