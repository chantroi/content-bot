import discord

basic = discord.SlashCommand("basic", "Basic Commands")

@basic.command()
async def content(ctx):
    await ctx.respond("Đây là Content Download phiên bản Discord")
    
@basic.command()
async def test(ctx):
    await ctx.respond("Test")

def setup(bot):
    bot.add_application_command(basic)