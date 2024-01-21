import discord

basic = discord.SlashCommandGroup("basic", "Basic Commands")

@basic.command()
async def content(ctx):
    await ctx.respond("Đây là Content Download phiên bản Discord")
    
async def setup(bot):
    bot.add_application_command(basic)