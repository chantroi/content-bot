from discord.ext import commands
from init import bot_token
import discord

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(
    description="Content Download",
    intents=intents,)

bot.load_extension("commands.basic")
bot.run(bot_token)